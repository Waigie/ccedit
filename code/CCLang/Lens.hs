module Lens where

import Control.Applicative ((<*))
import Data.List (intercalate,intersperse,nub)

import Text.Parsec hiding (choice,runParser)
import Text.Parsec.String
import Text.Parsec.Token
import Text.Parsec.Language (emptyDef)


--
-- * Language Implementationn
--

-- | Dimension name.
type Dim = String

-- | Choice calculus syntax.
data CC a = Obj a
          | Chc Dim (CC a) (CC a)
  deriving (Eq,Ord)

instance Show a => Show (CC a) where
  show (Obj a)     = show a
  show (Chc d l r) = concat [d, "<", show l, ",", show r, ">"]

-- | Selector.
type Sel = (Dim,Bool)

-- | Select a single dimension.
select :: Sel -> CC a -> CC a
select s@(d,t) (Chc d' l r)
  | d == d'   = select s (if t then l else r)
  | otherwise = Chc d' (select s l) (select s r)
select _ e = e

-- | (Partial) configuration.
newtype Config = Config [Sel]
  deriving (Eq,Ord)

-- | (Paritally) configure a CC expression.
config :: Config -> CC a -> CC a
config (Config ss) e = foldr select e ss

instance Show Config where
  show (Config ss) = "[" ++ intercalate "," (map sel ss) ++ "]"
    where sel (d,t) = concat [d, ".", if t then "l" else "r"]

-- | All dimensions in a CC expression.
dims :: CC a -> [Dim]
dims (Obj _)     = []
dims (Chc d l r) = nub (d : (dims l ++ dims r))

-- | Get all complete configurations for a list of dimensions.
configs :: [Dim] -> [Config]
configs = map Config . confs
  where
    confs []     = [[]]
    confs (d:ds) = let cs = confs ds in
                   map ((d,True):) cs ++ map ((d,False):) cs

-- | Get all super-complete configurations for two expressions.
super :: CC a -> CC a -> [Config]
super l r = configs (nub (dims l ++ dims r))

-- | Lookup a dimension in a configuration.
look :: Dim -> Config -> Maybe Bool
look d (Config ss) = lookup d ss

-- | A mapping from complete configurations to plain values.
sem :: CC a -> [(Config,a)]
sem e = [(c, plain (config c e)) | c <- configs (dims e)]
  where plain (Obj a) = a

-- | Semantic equivalence.
equiv :: Eq a => CC a -> CC a -> Bool
equiv l r = all (\c -> config c l == config c r) (super l r)

-- | Semantic inequivalence.
nequiv :: Eq a => CC a -> CC a -> Bool
nequiv l r = not (equiv l r)


--
-- * Lens
--

-- | Vary a value with respect to a (partial) configuration.
choice :: Config -> CC a -> CC a -> CC a
choice (Config ss) new old = chc ss
  where
    chc []             = new
    chc ((d,True) :ss) = Chc d (chc ss) old
    chc ((d,False):ss) = Chc d old (chc ss)

minimize :: CC a -> CC a
minimize (Obj a)     = Obj a
minimize (Chc d l r) = Chc d (minimize (select (d,True)  l))
                             (minimize (select (d,False) r))

-- | Update a source with a view.
update :: Config -> CC a -> CC a -> CC a
update c src view' = minimize (choice c view' src)

-- | True if the second configuration is a completion of the first.
subConfig :: Config -> Config -> Bool
subConfig (Config []) _ = True
subConfig (Config ((d,t):ss)) c
  | Just u <- look d c = if t == u then subConfig (Config ss) c else False
  | otherwise = error "subConfig: dims of first arg must be subset of second"

-- | Check whether an update is consistent. This is the essential property
--   that the update function should preserve.
check :: Eq a => Config -> CC a -> CC a -> CC a -> Bool
check proj src src' view' = all chk (super src src')
  where
    chk c | subConfig proj c = config c src' == config c view'
          | otherwise        = config c src' == config c src


--
-- * Simple parser for (CC Int)
--

lexer = makeTokenParser emptyDef

parseCC :: Parser (CC Int)
parseCC = try parseChc <|> fmap Obj parseInt

parseInt :: Parser Int
parseInt = fmap fromInteger (integer lexer)

parseDim :: Parser Dim
parseDim = identifier lexer

parseChc :: Parser (CC Int)
parseChc = do
    d <- parseDim <* char '<'
    l <- parseCC  <* char ','
    r <- parseCC  <* char '>'
    return (Chc d l r)

parseSel :: Parser Sel
parseSel = do
    d <- parseDim
    char '.'
    t <- try (char 'l' >> return True) <|>
             (char 'r' >> return False)
    return (d,t)

parseConfig :: Parser Config
parseConfig = fmap Config (parseSel `sepBy` char ',')

runParser :: Parser a -> String -> a
runParser p = either (error . show) id . parse (p <* eof) ""

readCC :: String -> CC Int
readCC = runParser parseCC

readConfig :: String -> Config
readConfig = runParser parseConfig


--
-- * Test cases
--

type TestCase = (CC Int, Config, CC Int, CC Int, CC Int)

testCase :: String -> String -> String -> String -> String -> TestCase
testCase s p v v' s' = (readCC s, readConfig p, readCC v, readCC v', readCC s')

checkCase :: TestCase -> Bool
checkCase (src, proj, _, view', src') = check proj src src' view'

runCase :: TestCase -> String
runCase (src, proj, view, view', src') =
  unwords ["config", show proj, show src,
           "\n  Exp:", show view,
           "\n  Got:", show (config proj src),
           "\nupdate", show proj, show src, show view',
           "\n  Exp:", show src',
           "\n  Got:", show (update proj src view')]

runCases :: [TestCase] -> IO ()
runCases = mapM_ putStrLn . intersperse "" . map runCase

test :: TestCase -> String
test (src, proj, view, view', src')
    | config proj src `nequiv` view =
        unwords ["Error: config", show proj, show src,
                 "\n  Exp:", show view,
                 "\n  Got:", show (config proj src)]
    | update proj src view' `nequiv` src' =
        unwords ["Error: update", show proj, show src, show view',
                 "\n  Exp:", show src',
                 "\n  Got:", show (update proj src view')]
    | otherwise = "Success"

runTests :: [TestCase] -> IO ()
runTests = mapM_ (putStrLn . test)

runAll = do putStrLn "** Leaves **"        >> runTests leaves
            putStrLn "** Subexpression **" >> runTests subs
            putStrLn "** Implicit **"      >> runTests implicit
            putStrLn "** Tricky **"        >> runTests tricky

-- | Edits that only change leaves. Correct behavior is obvious.
leaves = [
  testCase "A<1,2>"           "A.l"     "1"      "3"      "A<3,2>",
  testCase "A<1,2>"           "A.r"     "2"      "3"      "A<1,3>",
  testCase "A<1,2>"           "A.l"     "1"      "B<3,4>" "A<B<3,4>,2>",
  testCase "A<1,2>"           "A.r"     "2"      "B<3,4>" "A<1,B<3,4>>",
  testCase "A<1,B<2,3>>"      "A.l"     "1"      "4"      "A<4,B<2,3>>",
  testCase "A<1,B<2,3>>"      "A.l"     "1"      "B<4,5>" "A<B<4,5>,B<2,3>>",
  testCase "A<1,B<2,3>>"      "A.r,B.l" "2"      "4"      "A<1,B<4,3>>",
  testCase "A<1,B<2,3>>"      "A.r,B.r" "3"      "4"      "A<1,B<2,4>>",
  testCase "A<B<1,2>,B<3,4>>" "A.l,B.l" "1"      "5"      "A<B<5,2>,B<3,4>>",
  testCase "A<B<1,2>,B<3,4>>" "A.l,B.r" "2"      "5"      "A<B<1,5>,B<3,4>>",
  testCase "A<B<1,2>,B<3,4>>" "A.r,B.l" "3"      "5"      "A<B<1,2>,B<5,4>>",
  testCase "A<B<1,2>,B<3,4>>" "A.r,B.r" "4"      "5"      "A<B<1,2>,B<3,5>>"]

-- | Edits that modify choices but preserve the subexpression relationship.
--   Correct behavior seems clear.
subs = [
  testCase "A<1,B<2,3>>"      "A.r"     "B<2,3>" "4"      "A<1,4>",
  testCase "A<1,B<2,3>>"      "A.r"     "B<2,3>" "B<4,5>" "A<1,B<4,5>>",
  testCase "A<B<1,2>,B<3,4>>" "A.l"     "B<1,2>" "5"      "A<5,B<3,4>>",
  testCase "A<B<1,2>,B<3,4>>" "A.r"     "B<3,4>" "5"      "A<B<1,2>,5>",
  testCase "A<B<1,2>,B<3,4>>" "A.l"     "B<1,2>" "B<5,6>" "A<B<5,6>,B<3,4>>",
  testCase "A<B<1,2>,B<3,4>>" "A.r"     "B<3,4>" "B<5,6>" "A<B<1,2>,B<5,6>>",
  testCase "A<B<1,2>,B<3,4>>" "B.l"     "A<1,3>" "A<5,6>" "A<B<5,2>,B<6,4>>",
  testCase "A<B<1,2>,B<3,4>>" "B.r"     "A<2,4>" "A<5,6>" "A<B<1,5>,B<3,6>>"]

-- | Interesting cases because the edits preserve the subexpression
--   relationship but the update introduces new choices.
implicit = [
  testCase "1"                "A.l"     "1"      "2"      "A<2,1>",
  testCase "1"                "A.r"     "1"      "2"      "A<1,2>",
  testCase "1"                "A.l,B.l" "1"      "2"      "A<B<2,1>,1>",
  testCase "1"                "A.l,B.r" "1"      "2"      "A<B<1,2>,1>",
  testCase "1"                "A.r,B.l" "1"      "2"      "A<1,B<2,1>>",
  testCase "1"                "A.r,B.r" "1"      "2"      "A<1,B<1,2>>",
  testCase "A<1,B<2,3>>"      "B.l"     "A<1,2>" "A<4,5>" "A<B<4,1>,B<5,3>>", -- was: A<4,B<5,3>>
  testCase "A<1,B<2,3>>"      "B.r"     "A<1,3>" "A<4,5>" "A<B<1,4>,B<2,5>>"] -- was: A<4,B<2,5>>

-- | Edits that don't preserve the subexpression relationship.
--   Correct behavior may be non-obvious.
tricky = [
  testCase "A<1,B<2,3>>"      "B.l"     "A<1,2>" "4"      "B<4,A<1,3>>", -- was B<4,3>
  testCase "A<1,B<2,3>>"      "B.r"     "A<1,3>" "4"      "B<A<1,2>,4>", -- was B<2,3> ... why?
  testCase "A<B<1,2>,B<3,4>>" "B.l"     "A<1,3>" "5"      "A<B<5,2>,B<5,4>>",
  testCase "A<B<1,2>,B<3,4>>" "B.r"     "A<2,4>" "5"      "A<B<1,5>,B<3,5>>"]
