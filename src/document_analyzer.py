from typing import List, Dict
from transformers import pipeline
from github import Github

def read_documents(owner: str, repo: str, branch: str, data_dir: str = "data/") -> List[Dict[str, str]]:
    """
    Reads documents from the specified directory in the repository.

    Args:
        owner: Repository owner (username or organization).
        repo: Repository name.
        branch: Branch to read documents from.
        data_dir: Directory containing the documents.

    Returns:
        A list of dictionaries, where each dictionary contains the document's
        filename and content.
    """
    documents = []
    try:
        # Get the repository using PyGithub
        g = Github()
        repository = g.get_repo(f"{owner}/{repo}")

        # Get the contents of the data directory
        contents = repository.get_contents(data_dir, ref=branch)

        for content_file in contents:
            if content_file.name.endswith(".txt") or content_file.name.endswith(".md"):
                try:
                    # Get the file content
                    file_content = content_file.decoded_content.decode()
                    documents.append({"filename": content_file.name, "content": file_content})
                except Exception as e:
                    print(f"Error reading file {content_file.name}: {e}")
    except Exception as e:
        print(f"Error reading directory {data_dir}: {e}")
    return documents

def extract_structure(document_content: str) -> List[Dict[str, str]]:
    """
    Extracts the textual structure from the given document content using an LLM.

    Args:
        document_content: The content of the document.

    Returns:
        A list of dictionaries, where each dictionary represents a structural
        element (e.g., heading, paragraph) and its content.
    """
    # Use a summarization pipeline to identify key structural elements
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(document_content, max_length=130, min_length=30, do_sample=False)

    # Split the summary into structural elements (this is a basic approach and can be improved)
    structural_elements = [{"type": "paragraph", "content": element} for element in summary[0]['summary_text'].split(". ")]

    return structural_elements