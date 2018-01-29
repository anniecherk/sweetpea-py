module Main where

import FrontEnd

main :: IO ()
main = do let color = Factor "color" [Level "red", Level "blue", Level "green"]
          let shape = Factor "shape" [Level "circle", Level "square"]
          let size  = Factor "size"  [Level "small",  Level "big"]

          let nTrials = 6

          let design = [color, shape, size]
          contents <- readFile "ex.res"
        --  fileName <- getLine
        --  contents <- readFile fileName
          putStrLn $ decode contents design nTrials
