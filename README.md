# Thue-interpreter-in-python
A thue interpreter that runs in python's console


Word definitions:
Rule = substitution rule
Output = string that is the output of the program
State = the current program state

Implementation specifications/clarifications:
--------------------------------------------
The list of substitution rules (from now on rules) ends with a line containing solely "::=" (two colons and an equals sign). This line is not counted as a rule line.
Every line after that is concatenated (the \n are removed).
There is no way to output a character that would make a new line at the moment.

Only the lines containing at least one "::=" in the list of rules are counted as rule lines. This means that they will later be set as rules by the interpreter.
The other lines are skipped. They can be used for better orientation or you can use them to make your code more tidy or organized.

Rule lines:
  The first "::=" separates the lhs (left hand side) and rhs (right hand side) such that: "lhs::=rhs" is the full line without the new line (\n) at the end.
  If the length of lhs is 0 (there are no symbols) then the interpreter ends with an Error, because there can not be a rule that would create new characters out of nothing (at the moment - can be implemented later ig).
  Otherwise it sets a rule such that lhs is to be replaced by rhs.
  If rhs is of length 0, then lhs will just be erased.
  Even whitespace characters count as symbols - you can replace " " (one space) with "  " (tabulator) or "  " (two spaces).
  If lhs is exactly ":::" (three colons), then the rule will be set to replace rhs with player's input.
  If the first character of rhs is "~" (tilde), then the rest of the rhs is added to the end of output.

How does the random applying of rules work:
  Each rule is specified as "before" to which corresponds an array of possible "after"s.
  There can not be the same "before".
  A list of "before"s is shuffled and we go through each "before" and if one is possible, then at a random possible position in the current state we substitute it with a random "after" from the corresponding array.
  If there is no applicable rule, the program ends and the output is printed.
  
  There are more possible random applications of rules and I will add them later (probably).

How you run the program:
  Everything is in the main() function.
  



