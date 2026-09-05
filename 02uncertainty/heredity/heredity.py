import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """

    def calcMode(x, y, z):
        """
         x -> has father and/or mother
         y -> has trait or not
         z -> prob to calculate
        """

        mother = people[person]['mother']
        father = people[person]['father']
            
        trait = True if y == 1 else False

        trait_factor = PROBS['trait'][z][trait]

        # Probabilities to the parents send a gene if we have information about them

        if mother in one_gene:
            probMother1 = 0.5 * 0.99 + 0.5 * 0.01
        elif mother in two_genes:
            probMother1 = 0.99
        else:
            probMother1 = 0.01

        if father in one_gene:
            probFather1 = 0.5 * 0.99 + 0.5 * 0.01
        elif father in two_genes:
            probFather1 = 0.99
        else:
            probFather1 = 0.01
        

        # Probabilities to the parents send a gene if we don't have information about them

        probFatherUnknown1 = 0
        probMotherUnknown1 = 0

        if people[person]['mother'] == None or people[person]['father'] == None:
            for i in range(3):
                p_gene = PROBS["gene"][i]
                if i == 0:
                    probMotherUnknown1 += p_gene * 0.01
                elif i == 1:
                    probMotherUnknown1 += p_gene * (0.5 * 0.99 + 0.5 * 0.01)
                elif i == 2:
                    probMotherUnknown1 += p_gene * 0.99
            
            probFatherUnknown1 = probMotherUnknown1
                    
        if x == 0:

            # The calc of all these probabilities will be a product, because the events that are being analysed are independents    
            return trait_factor * PROBS["gene"][z]
        
        if True:

            if z == 0:
                # Calculate the chance to this person has no gene
                if x == 1:
                    return (1-probMother1) * (1-probFather1) * trait_factor  
                if x == 2:
                    return (1-probFatherUnknown1) * (1-probMother1) * trait_factor               
                if x == 3:
                    return (1-probMotherUnknown1) * (1-probFather1) * trait_factor
                
            elif z == 1:
                # Calculate the chance to this person has one gene
                if x == 1:    
                    return probMother1 * (1-probFather1) * trait_factor + probFather1 * (1-probMother1) * trait_factor
                if x == 2:
                    return probMother1 * (1-probFatherUnknown1) * trait_factor + probFatherUnknown1 * (1-probMother1) * trait_factor
                if x == 3:
                    return probFather1 * (1-probMotherUnknown1) * trait_factor + probMotherUnknown1 * (1-probFather1) * trait_factor

            else:
                # Calculate the chance to this person has two genes
                
                if x == 1:
                    return probMother1 * probFather1 * trait_factor
                if x == 2:
                     return probMother1 * probFatherUnknown1 * trait_factor
                if x == 3:
                     return probFather1 * probMotherUnknown1 * trait_factor
       
    
        
        
    # Define the value 1 to result because the multiplication with one don't change the final result 

    result = 1

    for person in people:
        # Define the arguments to use in calcMode

        if people[person]['mother'] == None and people[person]['father'] == None:
            # Has no mother neither father
            calc_mode_value_x = 0
        elif people[person]['mother'] != None and people[person]['father'] != None:
            # Has father and mother
            calc_mode_value_x = 1
        elif people[person]['mother'] != None and people[person]['father'] == None:
            # Has only mother
            calc_mode_value_x = 2
        elif people[person]['mother'] == None and people[person]['father'] != None:
            # Has only father
            calc_mode_value_x = 3
        
        calc_mode_value_y = 1 if person in have_trait else 0

        if person in one_gene:
            calc_mode_value_z = 1
        elif person in two_genes:
             calc_mode_value_z = 2
        else:
            calc_mode_value_z = 0
        
        # The result the product of all the probabilities

        result = result * calcMode(calc_mode_value_x, calc_mode_value_y, calc_mode_value_z)

    return result


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    # Loop through probabilities to update each item

    for prob in probabilities:
        
        trait = True if prob in have_trait else False
        
        if prob in one_gene:

            probabilities[prob]['gene'][1] += p

        elif prob in two_genes:

            probabilities[prob]['gene'][2] +=  p

        else:

            probabilities[prob]['gene'][0] += p

        probabilities[prob]['trait'][trait] += p
  




def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    normalized_dict = probabilities.copy()
    
    properties = ['gene', 'trait']
    # To normalize a set of numbers we need to sum these numbers and divide each one by the sum Ex [0.1,0.2] 0.1 + 0.2 = 0.3  0.1 / 0.3 = 1/3 and 0.2 / 0.3 = 2/3
    for person in probabilities:
        for prop in properties:
            s = sum(probabilities[person][prop].values())
            for key in probabilities[person][prop].keys():
                normalized_dict[person][prop][key] = normalized_dict[person][prop][key] / s 

    return normalized_dict

            




if __name__ == "__main__":
    main()
