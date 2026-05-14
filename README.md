ComfyUI_EmAySee_CustomNodes
This repository contains a collection of custom nodes for ComfyUI developed by EmAySee.

**Currently AI Described these for me.. i'll update the descriptions later.

The custom nodes should now appear in the ComfyUI add node menu under their respective categories (mostly starting with "EmAySee_").
Nodes Included
Here is a brief description of each custom node in this repository:

**EmAySee_CheckboxFloatNode.py**

	•	Node Title: EmAySee Checkbox Float

	•	Category: EmAySee_Utils

	•	Description: Likely provides a boolean input (checkbox) that controls a float output, possibly switching between two float values or enabling/disabling a float value based on the checkbox state.

**EmAySee_DateTimeStringNode.py**

	•	Node Title: EmAySee Date Time String

	•	Category: EmAySee_Utils

	•	Description: Generates a string representing the current date and time. Useful for timestamping outputs or incorporating time information into prompts.

**EmAySee_DynamicStringSelectorNode.py**

	•	Node Title: EmAySee Dynamic String Selector

	•	Category: EmAySee_String

	•	Description: Allows selection from a list of strings that can potentially be dynamically generated or input, offering more flexibility than a fixed dropdown.

**EmAySee_HostPinger.py**

	•	Node Title: EmAySee Host Pinger

	•	Category: EmAySee_Network

	•	Description: Pings a specified hostname or IP address and outputs an integer (1 for reachable, 0 for unreachable). Useful for conditional workflows based on network status.

**EmAySee_IntegerStringSelectorNode.py**

	•	Node Title: EmAySee Integer String Selector

	•	Category: EmAySee_String

	•	Description: Selects a string output based on an integer input, likely using the integer value to index into a list of predefined strings.

**EmAySee_IntegerStringSelectorNodeDynamic.py**

	•	Node Title: EmAySee Integer String Selector Dynamic

	•	Category: EmAySee_String

	•	Description: Similar to EmAySee_IntegerStringSelectorNode, but likely allows the list of strings to be dynamically input or generated.

**EmAySee_ProbabilityStringSelectorNode.py**

	•	Node Title: EmAySee Probability String Selector

	•	Category: EmAySee_String

	•	Description: Selects a string from a list based on a probabilistic distribution or a random selection influenced by probability settings.

**EmAySee_RandomIntFromList.py**

	•	Node Title: EmAySee Random Int From List

	•	Category: EmAySee_Utils

	•	Description: Selects and outputs a random integer from a provided list of integers.

**EmAySee_RandomIntFromList2.py**

	•	Node Title: EmAySee Random Int From List 2

	•	Category: EmAySee_Utils

	•	Description: Likely another version or variation of EmAySee_RandomIntFromList.py, potentially with different input methods or features for selecting a random integer from a list.

**EmAySee_RandomIntegerFromListNode.py**

	•	Node Title: EmAySee Random Integer From List

	•	Category: EmAySee_Utils

	•	Description: Another node for selecting a random integer from a list, possibly with different input/output types or controls compared to the other random integer list nodes.

**EmAySee_RandomIntegerFromTogglesNode_PremadeLabels.py**

	•	Node Title: EmAySee Random Integer From Toggles Premade Labels

	•	Category: EmAySee_Utils

	•	Description: Selects a random integer based on the state of multiple toggle (boolean) inputs, using predefined labels for the toggles.

**EmAySee_RandomStringSelectorNode.py**

	•	Node Title: EmAySee Random String Selector

	•	Category: EmAySee_String

	•	Description: Selects and outputs a random string from a provided list of strings.

**EmAySee_RandomStringSelectorNode2.py**

	•	Node Title: EmAySee Random String Selector 2

	•	Category: EmAySee_String

	•	Description: Likely a second version or variation of EmAySee_RandomStringSelectorNode.py.

**EmAySee_RandomStringSelectorNodeFourChoice.py**

	•	Node Title: EmAySee Random String Selector Four Choice

	•	Category: EmAySee_String

	•	Description: Specifically designed to select a random string from a fixed set of four choices.

**EmAySee_RandomStringSelectorNodeThreeChoice.py**

	•	Node Title: EmAySee Random String Selector Three Choice

	•	Category: EmAySee_String

	•	Description: Specifically designed to select a random string from a fixed set of three choices.

**EmAySee_RemoveDuplicateCSV.py**

	•	Node Title: EmAySee Remove Duplicate CSV

	•	Category: EmAySee_Text

	•	Description: Takes a string containing comma-separated values (CSV) and removes any duplicate entries, outputting a cleaned CSV string.

**EmAySee_RepaintKSampler.py**

	•	Node Title: EmAySee Repaint KSampler

	•	Category: EmAySee_Repaint

	•	Description: A specialized KSampler node designed for image repainting using a mask. It takes a latent image and a mask as input and performs sampling primarily in the masked (white) areas to add detail or change content while preserving the unmasked (black) areas.

**EmAySee_SaveImage.py**

	•	Node Title: EmAySee Save Image

	•	Category: EmAySee_Image

	•	Description: Saves an input image to a specified location on disk, with out worrying about if it's in Comfy path or not.

**EmAySee_StringPoseSelectorNode.py**

	•	Node Title: EmAySee String Pose Selector

	•	Category: EmAySee_String

	•	Description: Likely selects a string representation of a pose or pose-related parameter, possibly from a predefined list or based on input.

**EmAySee_StringTupleInputNode.py**

	•	Node Title: EmAySee String Tuple Input (DEV NODE, Wouldn't use it)

	•	Category: EmAySee_Utils

	•	Description: Allows input of multiple strings as a tuple, useful for grouping related string data.

**EmAySee_SubmitToOobaboogaAPI.py**

	•	Node Title: EmAySee Submit To Oobabooga API

	•	Category: EmAySee_Network

	•	Description: Sends a text prompt or other data to an Oobabooga Text Generation Web UI API endpoint and outputs the response. Useful for integrating large language models into workflows.

**EmAySee_ToggleIntNode.py**

	•	Node Title: EmAySee Toggle Int

  	•	Category: EmAySee_Utils

  	•	Description: A node with a toggle (checkbox) that outputs one of two predefined integer values based on the toggle's state.

**EmAySee_VarTextReplacer.py**

	•	Node Title: EmAySee Var Text Replacer

	•	Category: EmAySee_Text

	•	Description: This node allows you to create a main text string containing placeholders in the format %var1% through %var10%. It provides 10 corresponding string input fields (var1 to var10). The node replaces each placeholder in the main text with the value from its corresponding input field, outputting the final combined string. Ideal for generating dynamic prompts or text based on workflow variables.

**EmAySee_VeryUniqueStringSelectorNode.py**

	•	Node Title: EmAySee Very Unique String Selector

	•	Category: EmAySee_String

	•	Description: Based on the name, this node likely provides a method for selecting a string that ensures uniqueness or is chosen based on a specific, potentially complex, selection logic.



Feel free to explore the code for each node for more details on their implementation.  Know before you go... Code provided without any garuntees or warranties or support.

