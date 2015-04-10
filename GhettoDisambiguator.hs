#!/usr/bin/env runhaskell
import PGF
import System.Environment
import Control.Applicative
import Data.Maybe
import Data.List

type Sentence = String
type Word     = String

main = do
    args <- getArgs
    if length args == 2 then do
        [p, l] <- getArgs
        pgf <- readPGF p
        loop $ fromMaybe (\x -> x :: String) $ (startStuff pgf) <$> (readLanguage l)
        else do
            [p, l, s] <- getArgs
            pgf <- readPGF p 
            putStrLn $ fromMaybe "" $ (startStuff pgf) <$> (readLanguage l) <*> pure s

getWord :: Bool -> String -> String
getWord _ ('^':xs)   = getWord True xs
getWord _ ('/':xs)   = ' ' : getWord False xs
getWord False (x:xs) = getWord False xs
getWord True (x:xs)  = x : getWord True xs
getWord _ "" = ""

parseSentence :: String -> [String]
parseSentence = words . getWord False

loop :: (String -> String) -> IO ()
loop parse = do
    s <- getLine
    if s == "quit" then putStrLn "bye" else do
        putStrLn $ parse s
        loop parse

getMorph :: PGF -> Language -> Word -> [(Lemma, Analysis)]
getMorph p l s = lookupMorpho (buildMorpho p l) s

initStream :: PGF -> Language -> Sentence -> [Tree] -> Morpho -> Word -> String
initStream p l orig pt m s
    | length morph > 0  = "^" ++ s ++ buildStream p l morph orig pt
    | otherwise         = "^" ++ s ++ "/*" ++ s ++ "$ "
    where morph = lookupMorpho m s 

buildStream :: PGF -> Language -> [(Lemma, Analysis)] -> Sentence -> [Tree] -> String
buildStream _ _ [] _ _ = "$ "
buildStream p ln ((l, a):xs) s pt
    | isValid pt l = "/" ++ show l ++ buildTags (words a) ++ buildStream p ln xs s pt
    | otherwise = buildStream p ln xs s pt

isValid :: [Tree] -> Lemma -> Bool
isValid pt l = isInfixOf (show l) . show $ (head $ filter (\x -> not $ isInfixOf "LStr" (show x)) pt)

buildTags :: [String] -> String
buildTags [] = ""
buildTags (x:xs) = "<" ++ x ++ ">" ++ buildTags xs 

parseString :: PGF -> Language -> [Tree] -> Morpho -> Sentence -> String
--parseString p l s = foldl (\acc x -> acc ++ x) "" (map (initStream p l (getWord False s)) (parseSentence s))
parseString p l pt m s = foldl (\acc x -> acc ++ x) "" (map (initStream p l s pt m) (words s))

startStuff :: PGF -> Language -> Sentence -> String
startStuff p l s = parseString p l (parse p l (startCat p) s) (buildMorpho p l) s
