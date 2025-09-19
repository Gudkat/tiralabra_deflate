# Week 2 report

Finished huffman decoding and refactored code.

| Date       | Time Used | Description of Activities|
|------------|------------|----------------------|
| 16.9. | 3h | started on huffman decoding |
| 17.9. | 3h | otherwise completed huffman decoding, header zeros decode into extra character |
| 18.9. | 5h | Finished huffman decoding. Bunch of refactoring |
| 19.9. | 1h | Wrote basic unittests for huffman encoding and decoding. Improved code to handle couple of edge cases. |

## Questions

* Is it enough to test that there is meaningful compression (like just test that there is f.ex. over 30% compression on general text or something...) or do should to like download some other github project on huffman and test compression ratios on it and use that as benchmark against my compression ratios on my test data..?
* I wrote my huffman encoding to work on utf-8 symbols for now. This added some extra bits on the tree encoding, but it might make actual compression smaller (my test data doesn't include non ASCII at the moment though). Does that make sense or should I rewrite some of it and do the compression just byte by byte and ignore the character encoding..?