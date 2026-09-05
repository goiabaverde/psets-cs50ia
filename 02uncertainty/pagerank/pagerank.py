import os
import random
import re
import sys
import numpy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    probability_distribution = dict()
    N = len(corpus.keys())

    for key in corpus.keys():
        probability_distribution[key] = (1-damping_factor)/N 
        if key in corpus[page]:
            probability_distribution[key] += damping_factor/(len(corpus[page]))
    return probability_distribution




def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Initialize the PageRank dictionary, and choose a random page with randint
    page_rank = transition_model(corpus, list(corpus)[random.randint(0, len(corpus.keys())-1)], damping_factor)

    # Do the n-1 remaining samples
    for i in range(n-1):
        temp = transition_model(corpus=corpus, page=random.choices(list(corpus.keys()), weights = list(page_rank.values()), k = 1)[0], damping_factor=damping_factor)
        for key in temp.keys():
            page_rank[key] += temp[key]

    # Divide by n to normalize the sum of the PageRank to 1
    for key in corpus.keys():
        page_rank[key] = page_rank[key]/n

    return page_rank

    


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    listCorpus = list(corpus)
    listPagesConverged = dict()
    pr = dict()
    
    def checkIfAllConverged(list):
        """
        This function returns True if all the PageRank values for each page converged; otherwise, this function will return False.
        """
        for value in list.values():
            if value == False:
                return False
        return True
    
    

    def findPagesThatLink(centralPage):
        """
        Return all the pages in a set that link to the page that has been passed as the argument.
        """
        result = set()
        for page in listCorpus:
            if centralPage in corpus[page]:
                result.add(page)
        return result

    
    # Initialize the PageRank dictionary and the dictionary that tracks the pages that converged
    pr = {key : (1/len(listCorpus)) for key in listCorpus}
    listPagesConverged = {key : False for key in listCorpus}

    COMUN_FACTOR = (1-damping_factor)/len(listCorpus)

    while checkIfAllConverged(listPagesConverged) == False:
        for page in listCorpus:
            initialValue = pr[page]
            pagesThatLink = findPagesThatLink(page)
            if(len(pagesThatLink) == 0):
                pr[page] = COMUN_FACTOR
                listPagesConverged[page] = True
            else:
                sum = 0
                for pg in pagesThatLink:
                    sum += (pr[pg] / len(corpus[pg]))
                newValue = COMUN_FACTOR + (damping_factor * sum)
                pr[page] = newValue 
                if abs(newValue - initialValue) < 0.001:
                    listPagesConverged[page] = True
    
    # Normalize PageRank values
    totalPR = numpy.sum(list(pr.values()), dtype = numpy.float32)
    for page in pr:
        pr[page] = pr[page] / totalPR
    return pr


if __name__ == "__main__":
    main()