#!/usr/bin/env runhaskell
import PGF
import System.Environment
import Control.Applicative
import Data.Maybe
import Data.List

main = do
    args <- getArgs
    if length args == 2 then do
        [p, l] <- getArgs
        pgf <- readPGF p
        loop $ fromMaybe (\x -> x :: String) $ (parseString pgf) <$> (readLanguage l)
        else do
            [p, l, s] <- getArgs
            pgf <- readPGF p 
            putStrLn $ fromMaybe "" $ (parseString pgf) <$> (readLanguage l) <*> pure s

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

getMorph :: PGF -> Language -> String -> [(Lemma, Analysis)]
getMorph p l s = lookupMorpho (buildMorpho p l) s

initStream :: PGF -> Language -> String -> String -> String
initStream p l orig s
    | length morph > 0  = "^" ++ s ++ buildStream p l morph orig
    | otherwise         = "^" ++ s ++ "/*" ++ s ++ "$ "
    where morph = getMorph p l s

buildStream :: PGF -> Language -> [(Lemma, Analysis)] -> String -> String
buildStream _ _ [] _ = "$ "
buildStream p ln ((l, a):xs) s
    | isValid p ln s l = "/" ++ show l ++ buildTags (words a) ++ buildStream p ln xs s
    | otherwise = buildStream p ln xs s
    where t = startCat p

isValid :: PGF -> Language -> String -> Lemma -> Bool
isValid p ln s l = isInfixOf (show l) . show $ (head $ filter (\x -> not $ isInfixOf "LStr" (show x)) (parse p ln t s))
    where t = startCat p

buildTags :: [String] -> String
buildTags [] = ""
buildTags (x:xs) = "<" ++ x ++ ">" ++ buildTags xs 

parseString :: PGF -> Language -> String -> String
parseString p l s = foldl (\acc x -> acc ++ x) "" (map (initStream p l (getWord False s)) (parseSentence s))

