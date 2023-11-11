# gd

go to definition.. sound simple enough?

This program attempts to solve a very specific problem.
The `go to definition` problem as well as the `list cross-references` problem

The input is:

	- the symbol we searching
	- the absolute file path we are in
	- the line and col numbers we ar at
	- the action
		- `goto definition`
		- `list cross references`

The output is:

	- one or more locations in the folowing format:
		- `<file_abs_path>:<line_number>:<col_number>`

The challenge that it faces is as follows:

	- it needs to be FAST
	- does NOT require LSP or other heavy cofigured solutions
	- auto detect the language of which the symbol is at
	- language specific challenges:
		- c:
			- MACROs are a pain in the ass
		- smali:
		- cpp:

## Existing solutions:
- ctags: the only 'real' solution that isn't working all the time..
- cscope: like ctags only worst.
- LSP: lets not even start...

## 'gd' solution

there seems to be always something that doesn't work as expected with all of the
solutions above, so the only acceptable solution I could think of is automate
what i do by hand. which is 'smart' grep the repo:

- try and guess with ripgrep + treesitter parsing
	- the ripgrep pattern wil derive from the detected language
	- the treesitter parsing will look for some form of 'call_expression's in the
	  case of `cross-references` action, and 'function_definition' in the case of
	  `goto definition` action.
- when the above attemp fails which will happen alot, add a 'custom search'
  logic to the script in an easy way so that all consequence searchs will use the
  provided logic


