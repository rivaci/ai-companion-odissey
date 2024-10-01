from IPython.display import Image, display
import warnings

# save a graph to a file
def save_graph_to_file(graph, file_path, format='png'):
    try:
        # Normalize to lowercase for both file extension and format
        format = format.lower()
        file_extension = file_path.split('.')[-1].lower()

        # Only raise a warning if the normalized file extension doesn't match the format
        if file_extension != format:
            warnings.warn(f"File extension '{file_extension}' does not match the specified format '{format}'. Saving as {format} anyway.")
        
        with open(file_path, 'wb') as file:
            if format == 'png':
                file.write(graph.get_graph().draw_mermaid_png())
            elif format == 'svg':
                file.write(graph.get_graph().draw_mermaid_svg())
            else:
                raise ValueError(f"Unsupported format: {format}")
        
        print(f"Graph saved successfully at {file_path}")
    except Exception as e:
        print(f"Error saving graph: {e}")

# display the image in a Jupyter Notebook
def show_graph(graph):
    try:
        display(Image(graph.get_graph().draw_mermaid_png()))
    except Exception as e:
        print(f"Error displaying graph: {e}")