# Week 1 report

I chose the subject to be compression algorithms. I found out that deflate is the popular one these days so it seemed like a nice choice. 

Mostly I spent time this week reading wikipedia articles and watching youtube videos. 


| Date       | Time Used | Description of Activities|
|------------|------------|----------------------|
| 3.9. | 2h | Watching youtube to get started |
| 5.9. | 4h | Reading wikipedia and watching multiple youtube videos. Got initial idea how to work on this. Created repo and signed up for the course in labtool |


## Questions

* The entire deflate algorithm execution such as it is used in gzip etc. seems to be quite a lot of work. In the video ([This one](https://www.youtube.com/watch?v=SJPvNi4HrWQ)) I linked in the specification.md document they mention difficulty about some of the huffman encoding not fitting within 15 bit space that is allocated to those. Would it be considered a detriment to leave the specification document as is and work on huffman and LZ77 first, then create a deflate using fixed table for symbols instead of working on a dynamic one for that? 
* I don't really find much benefit for actual user interface for this project. Is it okay to just have it run in CLI with args..?