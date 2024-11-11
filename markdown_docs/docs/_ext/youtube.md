## FunctionDef get_size(d, key)
**get_size**: The function of get_size is to extract numerical values from string representations of sizes (like "100px" or "50%"), returning them as an integer and a string indicating the unit.
**parameters**: 
· parameter1: d - A dictionary containing size-related options, such as 'width' or 'height'.
· parameter2: key - The specific key in the dictionary to extract the size from.

**Code Description**: This function is designed to parse size values provided within dictionaries. It performs several checks and operations:
- First, it verifies if the specified `key` exists within the input `d`. If not, it returns `None`.
- Next, it uses a regular expression (`re.match`) to match the value associated with `key` against patterns such as numbers followed by 'px', '%', or no unit. The pattern `(\\d+)(|%|px)$` ensures that only valid size representations are processed.
- If the input string does not match the expected format, a `ValueError` is raised with an informative message.
- Finally, it returns the matched number as an integer and the matched unit (or 'px' if no unit was provided).

This function plays a crucial role in extracting numerical values from configuration dictionaries used by other parts of the codebase. Specifically, it is called in the `run` method of the `YouTube` class to process options like "width" and "height". This ensures that any size specifications are correctly parsed before being utilized.

**Note**: Ensure that all input keys match those expected in the dictionary; otherwise, `None` will be returned. Also, verify that the values provided for sizes follow the acceptable format (e.g., "100px", "50%") to avoid runtime errors.

**Output Example**: If called with `d = {'width': '300px'}` and `key = 'width'`, the function will return `(300, 'px')`. If `key` is not found in `d`, it returns `None`. If the value does not match the expected pattern (e.g., `d['width'] = 'invalid'`), a `ValueError` is raised.
## FunctionDef css(d)
**css**: The function of css is to convert a dictionary of style key-value pairs into a CSS string.
**parameters**: 
· parameter1: d (A dictionary where keys are style properties and values are corresponding property values.)

**Code Description**: 
The `css` function takes a dictionary `d` as input, where the keys represent CSS style properties, and the values represent their corresponding values. The function sorts these key-value pairs alphabetically by key, then joins them into a single string separated by semicolons (`;`). This resultant string is a valid CSS declaration block.

This function is called within the `visit_youtube_node` method to generate appropriate style attributes for HTML elements (specifically `<div>` and `<iframe>` tags). The styles are used to control the layout, dimensions, and positioning of embedded YouTube videos based on different conditions. For instance, if a width percentage is provided but no height, the function calculates the aspect ratio and sets the necessary padding-top and padding-bottom values to maintain the correct video aspect ratio.

The `css` function ensures that all style properties are correctly formatted as CSS declarations before being applied to the HTML elements, making it easier to manage and apply styles dynamically based on conditions such as video dimensions or aspect ratios.

**Note**: Ensure that the input dictionary `d` contains valid CSS property names and values. The function assumes that the keys in `d` are strings representing style properties (e.g., "padding-top", "width"), and the values are also strings representing their corresponding values (e.g., "100px").

**Output Example**: 
If the input dictionary is `{"width": "560px", "height": "315px"}`, the output of the function will be `"height: 315px; width: 560px;"`.
## ClassDef youtube
**youtube**: The function of `youtube` is to process directives related to embedding YouTube videos into reStructuredText documents.

**attributes**: This class does not have any explicitly defined attributes; it inherits from `nodes.General` and `nodes.Element`.

**Code Description**: 
The `youtube` class serves as a directive node in the Sphinx documentation system, specifically designed for handling directives that embed YouTube videos. It is instantiated with parameters such as an ID (which likely corresponds to the YouTube video identifier), aspect ratio, width, and height.

- **Parameter1: id**
  - The `id` parameter represents the unique identifier of the YouTube video being embedded.
  
- **Parameter2: aspect**
  - The `aspect` parameter is optional. If provided, it specifies the aspect ratio of the video in the form of a tuple `(width, height)`. This parameter is validated using a regular expression to ensure that the input matches the expected format (e.g., "16:9").
  
- **Parameter3: width**
  - The `width` parameter specifies the width of the embedded YouTube video. It can be set explicitly or derived from other options.
  
- **Parameter4: height**
  - The `height` parameter specifies the height of the embedded YouTube video. Similar to `width`, it can be set explicitly or inferred based on other options.

The `run` method processes these parameters and returns a list containing a new instance of the `youtube` node, which is then used by Sphinx to render the directive into an HTML document. The `get_size` function is utilized to determine the width and height of the video based on the provided options or default values if no explicit values are given.

**Note**: 
- The `setup` method in the project registers the `youtube` node with Sphinx, making it available for use in reStructuredText documents.
- Ensure that all required parameters like aspect ratio, width, and height are correctly specified to avoid errors during rendering.
## FunctionDef visit_youtube_node(self, node)
**visit_youtube_node**: The function of visit_youtube_node is to generate HTML markup for embedding YouTube videos based on node attributes.
· parameter1: node (A dictionary containing metadata about the YouTube video node, including properties like "aspect", "width", and "height".)
**Code Description**: 

The `visit_youtube_node` method processes a node object that contains information such as aspect ratio ("aspect"), width, and height of a YouTube video. Based on these attributes, it constructs HTML elements to embed the video with appropriate styles.

1. **Initial Attribute Extraction**:
   - The function first retrieves the "aspect", "width", and "height" values from the node dictionary.
   - If no aspect ratio is provided, it defaults to 16:9 (a common standard for YouTube videos).

2. **Div Element Styling**:
   - Depending on whether width or height are specified, different styles are applied to a `<div>` element that acts as a container for the video. 
   - If only the width is provided and it's in percentage form, padding-top and padding-bottom values are calculated based on the aspect ratio to maintain the correct video aspect.
   - The `css` function is used to generate CSS style strings for both the `<div>` and `<iframe>` elements.

3. **Iframe Element Styling**:
   - If no height is provided but width is, then it calculates the appropriate height based on the aspect ratio.
   - Similarly, if only height is specified without a width, it calculates the corresponding width.
   - The `css` function again plays a role in formatting these styles into valid CSS strings.

4. **Attributes Setup**:
   - For the `<iframe>` element, source (`src`) and style attributes are set to embed the video from YouTube with proper dimensions and aspect ratio.
   - Additional attribute "allowfullscreen" is also added to enable full-screen functionality for the embedded video.

5. **HTML Markup Generation**:
   - The method generates the necessary HTML tags: a `<div>` element styled according to `div_style`, and an `<iframe>` element styled as per `style`.
   - These elements are appended to the body of the document, effectively embedding the YouTube video with specified or calculated dimensions.

The function ensures that the embedded video maintains its aspect ratio while fitting into the available space, providing a consistent user experience regardless of how the container is sized. This approach leverages dynamic calculations and conditional logic to handle various input scenarios gracefully.

**Note**: Ensure that the node dictionary contains valid CSS property names and values for the `css` function to work correctly. The method assumes that "id", "aspect", "width", and "height" are present in the node dictionary, with appropriate data types (e.g., tuples for dimensions).
## FunctionDef depart_youtube_node(self, node)
**depart_youtube_node**: The function of depart_youtube_node is to process or handle nodes related to YouTube content.

**Parameters**:
· node: This parameter represents the specific node that needs to be processed or handled within the context of YouTube content.

**Code Description**:
The `depart_youtube_node` method is a callback function designed to be invoked during the processing or rendering phase of nodes associated with YouTube content. It serves as an interface for customizing how such nodes are treated, allowing developers to add specific behaviors or transformations before they are rendered or further processed in the document generation pipeline.

In more detail, this method receives a single parameter `node`, which is expected to be an object representing a node within the document structure that pertains to YouTube content. The function's body is currently empty (`pass`), indicating that no default implementation exists for handling these nodes. This suggests that any actual processing logic or behavior should be added by extending this method.

The purpose of defining such a method could vary depending on the broader context, but common use cases might include:
- Extracting metadata from YouTube links embedded in documents.
- Converting YouTube node content into a specific format (e.g., HTML, LaTeX).
- Applying custom styling or formatting to nodes related to YouTube content.
- Integrating additional functionality such as fetching and displaying YouTube video thumbnails or descriptions.

**Note**: Since the function body is currently empty (`pass`), developers should implement their own logic within this method to handle the specific requirements of processing YouTube-related nodes in their documents. Ensure that any custom logic respects the overall structure and flow of the document generation process to avoid disruptions or errors.
## FunctionDef visit_youtube_node_latex(self, node)
**visit_youtube_node_latex**: The function of visit_youtube_node_latex is to generate LaTeX code that embeds a YouTube video link within a formatted quote block.
**parameters**:
· parameter1: node (dict)
    - A dictionary containing the metadata for the YouTube node, specifically requiring an 'id' key to reference the unique identifier of the YouTube video.

**Code Description**: The function visit_youtube_node_latex processes a specific type of node that represents a YouTube video. It appends LaTeX code to the body of a document, creating a visually appealing block that includes the YouTube video link. Here is a detailed breakdown:
- `self.body.append(...)`: This line adds content to the current context (likely within a larger process like generating a document). The content being added here is specifically formatted for embedding a YouTube video.
- `'\\begin{quote}\\begin{center}\\fbox{\\url{https://youtu.be/%s}}\\end{center}\\end{quote}' % node['id']`: This string template creates the LaTeX code. Let's break it down:
    - `\\begin{quote}` and `\\end{quote}`: These commands create a block quote in LaTeX, which is used to set off quoted text.
    - `\\begin{center}` and `\\end{center}`: These commands center-align the content within the block quote.
    - `\\fbox{...}`: This command creates a framed box around the content inside it. In this case, the URL of the YouTube video is placed inside the box.
    - `\\url{https://youtu.be/%s}`: The `\url` command in LaTeX typesets URLs properly, ensuring that the link remains clickable and formatted correctly within the document.
    - `% node['id']`: This placeholder is replaced with the actual value of the 'id' key from the input dictionary. The `node['id']` retrieves the unique identifier for the YouTube video.

**Note**: Ensure that the input dictionary passed to this function contains a valid 'id' key, as it is crucial for generating the correct URL. Additionally, make sure the document processing context (`self.body`) is properly set up to append content in the desired manner.
## ClassDef YouTube
**YouTube**: The function of YouTube is to embed a video from YouTube into Sphinx documentation.

**attributes**:
· `has_content`: Set to True indicating that this directive can contain body text.
· `required_arguments`: Specifies that one required argument is needed, which will be the YouTube video ID.
· `optional_arguments`: Set to 0 indicating no optional arguments are allowed beyond the required ones.
· `final_argument_whitespace`: Set to False meaning there should not be any trailing whitespace after the last argument.
· `option_spec`: A dictionary specifying that options for this directive can include "width", "height", and "aspect", all of which must be provided as unchanged strings.

**Code Description**: The YouTube class is a custom Sphinx directive designed to embed videos from YouTube into documentation. When used in reStructuredText, it allows developers to specify the video ID and optionally customize its appearance using width, height, or aspect ratio settings.

The `run` method processes these options:
1. If an "aspect" option is provided, it validates the aspect ratio string to ensure it follows a valid 16:9 format (or similar) before converting it into a tuple of integers.
2. It retrieves the width and height values from the options, using predefined functions if necessary.
3. Finally, it returns a node representing an embedded YouTube video with the specified attributes.

The class inherits from `Directive`, which means it can be used within reStructuredText documents as a directive to include dynamic content like videos or other interactive elements.

**Note**: Ensure that the provided video ID is correct and valid for embedding. The aspect ratio must follow a specific format, such as "16:9", otherwise, an error will be raised. For custom width and height values, they should be specified without any units (e.g., just integers).

**Output Example**: An example of using the YouTube directive in reStructuredText could look like this:
```
.. youtube:: video_id
   :width: 800
   :height: 450
   :aspect: 16:9

This would embed a YouTube video with the specified ID and customize its size and aspect ratio according to the provided options.
### FunctionDef run(self)
**run**: The function of run is to process YouTube video embedding options and return a list containing an instantiated `youtube` node.

· parameter1: self - An instance of the `YouTube` class.
· parameter2: aspect - A string representing the aspect ratio of the video, if provided in the options. This can be None if not specified.
· parameter3: width - The width of the embedded YouTube video, derived from the options or set to a default value.
· parameter4: height - The height of the embedded YouTube video, derived from the options or set to a default value.

**Code Description**: 
The `run` method within the `YouTube` class is responsible for handling and processing various embedding options related to YouTube videos. Here’s a detailed breakdown:

1. **Aspect Ratio Handling**: If an "aspect" option is provided in `self.options`, it first extracts this aspect ratio using regular expressions (`re.match`). The regex pattern `(\\d+):(\d+)` ensures that the input matches the format of a width-to-height ratio, such as "16:9". If the input does not match this pattern, a `ValueError` is raised with an informative message. Otherwise, it converts the matched groups into integers and stores them as a tuple.

2. **Size Extraction**: The method then calls `get_size(self.options, "width")` to extract the width of the video from the options dictionary. Similarly, `get_size(self.options, "height")` is called to get the height. This ensures that any size specifications are correctly parsed before being utilized.

3. **Node Instantiation and Return**: Finally, a new instance of the `youtube` node class is created with the extracted or default values for the video ID, aspect ratio, width, and height. The method returns a list containing this instantiated node.

The `run` method plays a crucial role in ensuring that all necessary parameters are correctly processed before being used to render an embedded YouTube video within reStructuredText documents. It leverages `get_size` to handle size-related options, validating and converting them as needed.

**Note**: 
- Ensure that the aspect ratio provided matches the expected format (e.g., "16:9"). If not specified, a default value will be used.
- The width and height should be specified in pixels. If they are not explicitly set, `get_size` will determine appropriate values based on the options or use defaults.

**Output Example**: 
The method might return a list like `[<youtube node instance>]`, where `<youtube node instance>` is an instantiated object with properties such as video ID, width, height, and aspect ratio, depending on the input provided.
***
## FunctionDef unsupported_visit_youtube(self, node)
**unsupported_visit_youtube**: The function of unsupported_visit_youtube is to handle nodes related to YouTube content when an unsupported output format is detected.
**parameters**: 
· node: The node representing the YouTube content that needs to be processed.

**Code Description**: 
The `unsupported_visit_youtube` method is a part of a larger system, likely used in document processing or transformation. When this function encounters a node (`node`) associated with YouTube content within an unsupported output format, it performs specific actions:
1. It logs a warning message using the builder's `warn` method, indicating that the current node (representing YouTube content) is being skipped due to the unsupported format.
2. It raises a `nodes.SkipNode` exception to ensure that the processing of this node is halted and not included in the final output.

This approach helps maintain the integrity of the document processing by ensuring that unsupported content types are appropriately handled, preventing potential errors or inconsistencies in the output.

**Note**: Users should be aware that this function assumes the presence of a `builder` object with a `warn` method for logging warnings and using `nodes.SkipNode` to skip nodes. The function is crucial for maintaining robustness in document processing systems where different content types may require varying handling strategies based on supported output formats.
## FunctionDef setup(app)
**setup**: The function of setup is to register the `youtube` node and directive with Sphinx.
**parameters**: 
· app: This parameter represents the Sphinx application instance, which is used to add nodes and directives to the system.

**Code Description**: 

The `setup` function serves as an entry point for integrating custom functionality into the Sphinx documentation builder. Specifically, it registers the `youtube` node and directive with the Sphinx application (`app`). By adding these components, the function enables developers to use the `youtube` directive within reStructuredText documents to embed YouTube videos.

Here is a detailed breakdown of what the `setup` function does:
1. **Adding Nodes**: The first line of the function uses `app.add_node(youtube, **_NODE_VISITORS)`. This call adds the `youtube` node to the Sphinx application's registry. `_NODE_VISITORS` likely contains visitor methods that are necessary for processing nodes during the document building process.

2. **Adding Directives**: The second line of the function uses `app.add_directive("youtube", YouTube)`. Here, it registers the `YouTube` directive with the Sphinx application. This allows developers to use the `.. youtube::` syntax in their reStructuredText documents to embed YouTube videos.

By ensuring that both nodes and directives are registered during the setup phase of the Sphinx build process, this function facilitates the seamless integration of custom content like embedded YouTube videos into the documentation system.

**Note**: Developers must ensure that all dependencies for handling YouTube video embedding (such as `_NODE_VISITORS` and the `YouTube` directive) are correctly defined and available when the `setup` function is called. Additionally, any required parameters or options specified in the `YouTube` directive should be validated and handled appropriately to avoid errors during document rendering.
