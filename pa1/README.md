# information-retrieval
Repository for information retrieval

## Steps

define initial frontier as a queue and insert the seeds
access the url respecting the robots
normalize the url and mark as visited
crawl the website
store the data and add the links to the frontier
wait 100ms if the next url is from the same site

## Parallelization

Running multiple scripts simultaneously is not a good idea, because the visited site will not be available for all
Then:
Execute with threads
each thread will have an own thread and when it gets empty will grab ten elements from the queue and put in the own queue
every time the queue ends, also updates the visited set

when the doc store gets to 1000 pages, call a function to convert to the WARC format
