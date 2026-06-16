import pytest
from unittest.mock import patch, MagicMock, PropertyMock
from pathlib import Path
from src.tools.resume_reader import ResumeReaderTool
from src.agents.resume_agent import ResumeAgent, ResumeInfo

def test_resume_agent_empty_text():
    agent = ResumeAgent()
    with pytest.raises(ValueError, match="Resume text cannot be empty"):
        agent.process("   ")

def test_resume_agent_no_llm():
    agent = ResumeAgent()
    res = agent.process("John Doe\nPython Developer")
    assert res == {
        "skills": [],
        "projects": [],
        "education": [],
        "experience": []
    }

def test_resume_agent_with_llm():
    mock_llm = MagicMock()
    mock_structured = MagicMock()
    mock_result = ResumeInfo(
        skills=["Python", "FastAPI"], 
        projects=["CareerPilot Project"], 
        education=["BSc Computer Science"], 
        experience=["Software Engineer at TechCorp"]
    )
    mock_structured.invoke.return_value = mock_result
    mock_llm.with_structured_output.return_value = mock_structured
    
    agent = ResumeAgent(llm_client=mock_llm)
    res = agent.process("Some resume text content...")
    
    assert res["skills"] == ["Python", "FastAPI"]
    assert res["projects"] == ["CareerPilot Project"]
    assert res["education"] == ["BSc Computer Science"]
    assert res["experience"] == ["Software Engineer at TechCorp"]
    mock_structured.invoke.assert_called_once()

@patch('src.tools.resume_reader.Path.exists')
def test_read_missing_file(mock_exists):
    mock_exists.return_value = False
    with pytest.raises(FileNotFoundError):
        ResumeReaderTool.read_file("non_existent.pdf")

@patch('src.tools.resume_reader.Path.exists')
@patch('src.tools.resume_reader.Path.suffix', new_callable=PropertyMock)
def test_read_unsupported_format(mock_suffix, mock_exists):
    mock_exists.return_value = True
    mock_suffix.return_value = '.txt'
    with pytest.raises(ValueError, match="Unsupported file format"):
        ResumeReaderTool.read_file("file.txt")

@patch('src.tools.resume_reader.pdfplumber.open')
@patch('src.tools.resume_reader.Path.exists')
def test_read_pdf(mock_exists, mock_pdf_open):
    mock_exists.return_value = True
    
    mock_page1 = MagicMock()
    mock_page1.extract_text.return_value = "Page 1 text"
    mock_page2 = MagicMock()
    mock_page2.extract_text.return_value = "Page 2 text"
    
    mock_pdf = MagicMock()
    mock_pdf.pages = [mock_page1, mock_page2]
    mock_pdf_open.return_value.__enter__.return_value = mock_pdf
    
    # We patch Path.suffix dynamically by mocking the path object where it's created or just use a valid string name
    with patch.object(Path, 'suffix', '.pdf'):
        text = ResumeReaderTool.read_file("fake.pdf")
        assert "Page 1 text\nPage 2 text" == text

@patch('src.tools.resume_reader.docx.Document')
@patch('src.tools.resume_reader.Path.exists')
def test_read_docx(mock_exists, mock_docx_doc):
    mock_exists.return_value = True
    
    mock_para1 = MagicMock()
    mock_para1.text = "Paragraph 1"
    mock_para2 = MagicMock()
    mock_para2.text = "Paragraph 2"
    
    mock_doc_instance = MagicMock()
    mock_doc_instance.paragraphs = [mock_para1, mock_para2]
    mock_docx_doc.return_value = mock_doc_instance

    with patch.object(Path, 'suffix', '.docx'):
        text = ResumeReaderTool.read_file("fake.docx")
        assert "Paragraph 1\nParagraph 2" == text
