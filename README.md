ComfyUI_EmAySee_CustomNodes

This repository contains a collection of custom nodes for ComfyUI developed by EmAySee.
Installation

1.	Clone this repository into your ComfyUI/custom_nodes directory:

2.	cd ComfyUI/custom_nodes

3.	git clone https://github.com/EmAySee/ComfyUI_EmAySee_CustomNodes.git

4.	Restart your ComfyUI server.

The custom nodes should now appear in the ComfyUI add node menu under their respective categories (mostly starting with "EmAySee_").





Nodes Included

Here is a brief description of each custom node in this repository, based on the provided code:





**EmAySee_AnyPassthrough.py**

•	Node Title: EmAySee Any Passthrough

•	Category: EmAySee_Utils

•	Description: A simple passthrough node that accepts any data type as input and outputs the same data. Useful for renaming input connections in the workflow for clarity.




**EmAySee_CheckboxFloatNode.py**

•	Node Title: EmAySee Checkbox to Float

•	Category: EmAySee_Utils

•	Description: Takes a boolean input (checkbox) and outputs a float value (1.0 if checked, 0.0 if unchecked). Useful for converting boolean logic into a numerical value for other nodes.







**EmAySee_DateTimeStringNode.py**

•	Node Title: EmAySee Date Time Filename String - Seeded

•	Category: EmAySee_Utils

•	Description: Generates a string representing the current date and time, formatted for use in filenames (YYYYMMDDHHMMSS + tenths of a second). Includes a seed input, although the primary function is based on the current time.







**EmAySee_DynamicStringSelectorNode.py**

•	Node Title: EmAySee Dynamic String Selector Seeded V2

•	Category: EmAySee_Utils

•	Description: Allows selection from a variable number of string inputs that can be dynamically added. Selects the output string based on an integer index. Includes a seed for potential random selection or workflow control.







**EmAySee_HostPinger.py**

•	Node Title: EmAySee Host Pinger

•	Category: EmAySee_Network

•	Description: Pings a specified hostname or IP address and outputs an integer (1 if the host is reachable, 0 if unreachable). Useful for conditional workflows based on network status.







**EmAySee_ImagePassthrough.py**

•	Node Title: EmAySee Image Passthrough

•	Category: EmAySee_Utils

•	Description: A simple passthrough node for image data. Takes an image input and outputs the exact same image. Primarily used for renaming image input connections in the workflow for better organization.







**EmAySee_IntegerStringSelectorNode.py**

•	Node Title: EmAySee Integer String Selector

•	Category: EmAySee_Utils

•	Description: Selects one of four predefined string inputs based on an integer index (1 to 4) provided via a slider or number input.







**EmAySee_IntegerStringSelectorNodeDynamic.py**

•	Node Title: EmAySee Integer String Selector Max-20

•	Category: EmAySee_Utils

•	Description: Selects one of up to 20 dynamically added string inputs based on an integer index (1 to 20) provided via a slider.







**EmAySee_multiplier_node.py**

•	Node Title: EmAySee Multiplier Node

•	Category: EmAySee_Utils

•	Description: Features a slider (1.0 to 2.0) and two integer inputs. Outputs the result of multiplying each integer input by the slider value. Useful for scaling numerical parameters.







**EmAySee_ProbabilityStringSelectorNode.py**

•	Node Title: EmAySee Probability String Selector

•	Category: EmAySee_Utils

•	Description: Selects between two string inputs based on a specified probability (0.0 to 1.0). Useful for introducing controlled randomness in string selection.







**EmAySee_RandomIntFromList.py**

•	Node Title: EmAySee - Random Integer from List 2

•	Category: EmAySee/Utilities/List

•	Description: Selects and outputs a random integer from a list or range of integers provided as a string input (e.g., "1, 5, 10-15"). Includes seed control and an option to use system time for variability.







**EmAySee_RandomIntFromList2.py**

•	Node Title: EmAySee Vroom Random Integer from List 2

•	Category: EmAySee/Utilities/List

•	Description: Another node for selecting a random integer from a list or range provided as a string. Similar functionality to EmAySee_RandomIntFromList.py, also includes seed control and system time option. (Note: Has a different display name).







**EmAySee_RandomIntegerFromListNode.py**

•	Node Title: EmAySee Random Integer From List

•	Category: EmAySee_Utils

•	Description: Selects and outputs a random integer from a list of integers provided as a comma-separated string input. Includes basic error handling for invalid entries.







**EmAySee_RandomIntegerFromTogglesNode_PremadeLabels.py**

•	Node Title: EmAySee Random Integer From Toggles (Premade Labels)

•	Category: EmAySee_Utils

•	Description: Selects a random integer corresponding to one of up to 20 boolean toggle inputs that are enabled (checked). Uses premade labels for the toggles.







**EmAySee_RandomStringSelectorNode.py**

•	Node Title: EmAySee Random String Selector

•	Category: EmAySee_Utils

•	Description: Selects and outputs a random string from two provided string inputs.







**EmAySee_RandomStringSelectorNode2.py**

•	Node Title: EmAySee Random String Selector

•	Category: EmAySee_Utils

•	Description: Another node for selecting a random string from two provided string inputs. Identical functionality to EmAySee_RandomStringSelectorNode.py.







**EmAySee_RandomStringSelectorNodeFourChoice.py**

•	Node Title: EmAySee Random String SelectorFourChoice

•	Category: EmAySee_Utils

•	Description: Selects and outputs a random string from four provided string inputs.







**EmAySee_RandomStringSelectorNodeThreeChoice.py**

•	Node Title: EmAySee Random String SelectorThreeChoice

•	Category: EmAySee_Utils

•	Description: Selects and outputs a random string from three provided string inputs.







**EmAySee_RemoveDuplicateCSV.py**

•	Node Title: EmAySee Remove Duplicate CSV

•	Category: EmAySee_Utils

•	Description: Takes a string containing comma-separated values (CSV) and outputs a new string with duplicate entries removed.







**EmAySee_RepaintKSampler.py**

•	Node Title: EmAySee Repaint KSampler

•	Category: EmAySee_Utils

•	Description: A specialized KSampler node designed for image repainting using an image mask. It applies the mask to the latent image and performs sampling primarily in the masked areas.






**EmAySee_SaveImage.py**

•	Node Title: Save Image (EmAySee)

•	Category: EmAySee/Image

•	Description: Saves input images to a specified subfolder with customizable filename prefixes, postfixes, and timestamps. Includes metadata handling.







**EmAySee_SaveTextToFile.py**

•	Node Title: EmAySee Save Text to File

•	Category: EmAySee_Utils

•	Description: Saves a string input to a text file with a specified filename and optional subfolder within the ComfyUI output directory.







**EmAySee_StringPoseSelectorNode.py**

•	Node Title: EmAySee Pose Option Selector

•	Category: EmAySee_Utils

•	Description: Selects one of five predefined string options (likely representing pose categories) based on an integer index (1 to 5) via a slider.







**EmAySee_StringTupleInputNode.py**

•	Node Title: EmAySee String Tuple Input

•	Category: EmAySee_Utils

•	Description: Takes a multiline string input, splits it into individual lines, and outputs them as a tuple of strings.







**EmAySee_SubmitToOobaboogaAPI.py**

•	Node Title: EmAySee Submit to Oobabooga API Node

•	Category: EmAySee_Utils

•	Description: Submits a text prompt and parameters to a text-generation-webui (Oobabooga) /v1/completions API endpoint and outputs the API response as a string.







**EmAySee_ToggleIntNode.py**

•	Node Title: EmAySee Toggle to Integer

•	Category: EmAySee_Utils

•	Description: Takes a boolean toggle input and outputs one of two specified integer values based on whether the toggle is ON or OFF.







**EmAySee_VarTextReplacer.py**

•	Node Title: EmAySee Var Text Replacer

•	Category: EmAySee_Text

•	Description: Replaces placeholders (like %var1% through %var10%) in a main text string with values from up to 10 string input variables. Ideal for generating dynamic prompts or custom text fields where you just want to change a portion of the prompt, without digging through the whole prompt for the text.








**EmAySee_VeryUniqueStringSelectorNode.py**

•	Node Title: EmAySee REALLY Unique String Selector

•	Category: EmAySee_Utils

•	Description: Selects one of two predefined string inputs based on a dropdown menu selection. (Note: The class name is EmAySee_StringSelectorNode, but the display name and file name suggest it's intended to be a unique selector).



Feel free to explore the code for each node for more details on their implementation.
