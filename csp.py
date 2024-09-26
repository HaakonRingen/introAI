from typing import Any, Optional
from queue import Queue
import time


class CSP:
    def __init__(
        self,
        variables: list[str],
        domains: dict[str, set],
        edges: list[tuple[str, str]],
    ):
        """Constructs a CSP instance with the given variables, domains and edges.
        
        Parameters
        ----------
        variables : list[str]
            The variables for the CSP
        domains : dict[str, set]
            The domains of the variables
        edges : list[tuple[str, str]]
            Pairs of variables that must not be assigned the same value
        """
        self.variables = variables
        self.domains = domains
        self.edges = edges

        # Binary constraints as a dictionary mapping variable pairs to a set of value pairs.
        #
        # To check if variable1=value1, variable2=value2 is in violation of a binary constraint:
        # if (
        #     (variable1, variable2) in self.binary_constraints and
        #     (value1, value2) not in self.binary_constraints[(variable1, variable2)]
        # ) or (
        #     (variable2, variable1) in self.binary_constraints and
        #     (value1, value2) not in self.binary_constraints[(variable2, variable1)]
        # ):
        #     Violates a binary constraint
        self.binary_constraints: dict[tuple[str, str], set] = {}
        for variable1, variable2 in edges:
            self.binary_constraints[(variable1, variable2)] = set()
            for value1 in self.domains[variable1]:
                for value2 in self.domains[variable2]:
                    if value1 != value2:
                        self.binary_constraints[(variable1, variable2)].add((value1, value2))
                        self.binary_constraints[(variable1, variable2)].add((value2, value1))
                        
    def revise(self, Xi, Xy) -> bool:
        revised = False # Flag to track if any values have been removed from the domain 
        to_remove = [] # List to store values that need to be removed from a domain 
        
        # Iterate through each value in the domain of Xi
        for x in self.domains[Xi]:
            satisfies_costraint = False # Flag to track if the value satifies the constraint 
            
            # Check if the value x has any corresponding value in Xy that satisfies the constraint 
            for y in self.domains[Xy]:
                
                # if (x,y) satisifies the constraint, mark as satisifies 
                if (x,y) in self.binary_constraints[(Xi,Xy)]:
                    satisfies_costraint = True
                    break # exit the loop early if a satisfying value is found 
            
            # if no satisfying value satisifies the coinstraint, mark for removal 
            if not satisfies_costraint:
                to_remove.append(x) # Add x to the list of values to remove 
                revised = True # set revised flag true to indicating a change 
                
        # remove the marked values from the domain of Xi 
        for val in to_remove:
            self.domains[Xi].remove(val)
            
        return revised # return whether any values where removed 
                    
            
        
        
        

    def ac_3(self) -> bool:
        """Performs AC-3 on the CSP.
        Meant to be run prior to calling backtracking_search() to reduce the search for some problems.
        
        Returns
        -------
        bool
            False if a domain becomes empty, otherwise True
        """
        # initialize the queue with all arcs (edges) from the CSP
        queue = []
        for arc in self.edges:
            queue.append(arc) # add each edge to the queue
            
        # Process arcs until the arc is empty 
        while len(queue) > 0:
            Xi, Xy = queue.pop(0) # remove the first arc from the queue 
            
            # revise the domain of Xi based on the constrains with Xy
            if self.revise(Xi, Xy):
                
                # if the domain of Xi becomes empty after revision return falsee
                if len(self.domains[Xi]) == 0:
                    return False
                
                # enqueue all neighbors of Xi to check their constraints
                for edge in self.edges:
                    
                    # skip the current arc being processed 
                    if edge[0] == Xi and edge[1] == Xy:
                        continue 
                    # check for the reverse direction of the arc 
                    if edge[0] == Xy and edge[1] == Xi:
                        neighbor = edge[0] #get the neighbor available 
                        queue.append((neighbor,Xi)) # add the arc back to the queue for revising 
        
        print(self.domains)
                        
        return True # return true if all domains are consistent
            
        
                
            
    def is_consistent(self, var : str, value: Any, assignment: dict[str,Any]) -> bool:
        #Iterate through all the variables already assigned in the current assignment 
        for var2, value2 in assignment.items():
            if (var, var2) in self.binary_constraints:
                
            # if the value for var and value2 no not satisfy the constraint, then return false
                if (value,value2) not in self.binary_constraints[(var,var2)]:
                    return False
                
            # check the reverse direction for the constraint 
            elif (var2, var) in self.binary_constraints:
                
                # if the value2 for var2 and the value for var do not satisfy the constraint, then return false
                if (value2, value) not in self.binary_constraints[(var2,var)]:
                    return False
                
        # if all constrains are satisfied, return true
        return True

    def select_unassigned_variable(self, assignment: dict[str,Any]):
        # iterate thorugh the variables
        for var in self.variables:
            
            # return the first variable that are not in the current assignement 
            if var not in assignment:
                return var
            
    def backtracking_search(self) -> Optional[dict[str, Any]]:
        """Performs backtracking search on the CSP.
        
        Returns
        -------
        None | dict[str, Any]
            A solution if any exists, otherwise None
        """
        
        # ac_3 can be run prior to backtrach to reduce domain
        # if not self.ac_3():
        #     return None
                
            
        backtrack_calls = 0
        failures = 0
        start_time = time.time()
        
            
        def backtrack(assignment: dict[str, Any]):
            
            nonlocal backtrack_calls, failures
            backtrack_calls += 1
            
            
            # if all variables have been assigned to the assignment we are finished and can return the assignement
            if len(assignment) == len(self.variables):
                return assignment
        
            # select an unassigned variable to work with 
            var = self.select_unassigned_variable(assignment)
            
            # iterate over all values in the domain of the selected variable 
            for value in self.domains[var]:
                
                #check if the current value is consistent with the assignment 
                if self.is_consistent(var,value,assignment):
                    # add the variable and its value to the assignment
                    assignment[var] = value
                    
                    # recursive call on backtrack to attempt to complete the asignement 
                    result = backtrack(assignment)
                    # if a valid result is returned, propgate it back
                    if result is not None:
                        return result
                    # if the value doesn't lead to a solution, remove it from the assignment
                    del assignment[var]
                    
            failures += 1
            # return None if no valid assignment can be found    
            return None
        
        
        # Start the backtrach search with an empty dictionary
        solution = backtrack({})
        
        print(f"#Backtracks: {backtrack_calls}")
        print(f"#Failures: {failures}")
        
        end_time = time.time()
        total_time = end_time - start_time
        
        print(f"Backtrack time: {total_time}")
        
        return solution


def alldiff(variables: list[str]) -> list[tuple[str, str]]:
    """Returns a list of edges interconnecting all of the input variables
    
    Parameters
    ----------
    variables : list[str]
        The variables that all must be different

    Returns
    -------
    list[tuple[str, str]]
        List of edges in the form (a, b)
    """
    return [(variables[i], variables[j]) for i in range(len(variables) - 1) for j in range(i + 1, len(variables))]


