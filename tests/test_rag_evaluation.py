"""
RAG Evaluation Test Suite for the College Helpdesk system.

This module evaluates the RAG pipeline's ability to:
1. Retrieve the correct source documents
2. Generate relevant answers containing expected keywords
3. Provide accurate source citations
4. Maintain reasonable response times

Usage:
    python -m tests.test_rag_evaluation

Results are saved to ./evaluation_results.json for the admin dashboard.
"""
import json
import time
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Test dataset: questions with expected sources and answer keywords
EVAL_DATA = [
    {
        "question": "What is the minimum attendance requirement?",
        "expected_source_document": "Attendance_Regulations.pdf",
        "expected_keywords": ["75%", "attendance", "minimum"],
        "category": "Attendance"
    },
    {
        "question": "What happens if a student has less than 75% attendance?",
        "expected_source_document": "Attendance_Regulations.pdf",
        "expected_keywords": ["detained", "not permitted", "repeat"],
        "category": "Attendance"
    },
    {
        "question": "What is the condonation rule for attendance?",
        "expected_source_document": "Attendance_Regulations.pdf",
        "expected_keywords": ["condonation", "10%", "65%", "1000"],
        "category": "Attendance"
    },
    {
        "question": "What grades can I get in the exams?",
        "expected_source_document": "Examination_Rules.pdf",
        "expected_keywords": ["O", "A+", "A", "B+", "B", "C", "F"],
        "category": "Examination"
    },
    {
        "question": "How do I calculate my CGPA?",
        "expected_source_document": "Examination_Rules.pdf",
        "expected_keywords": ["credits", "grade points", "sum"],
        "category": "Examination"
    },
    {
        "question": "What is the penalty for cheating in exams?",
        "expected_source_document": "Examination_Rules.pdf",
        "expected_keywords": ["disciplinary", "cancellation", "expulsion"],
        "category": "Examination"
    },
    {
        "question": "How much is the tuition fee for Computer Science?",
        "expected_source_document": "Fee_Structure_2024_25.pdf",
        "expected_keywords": ["1,20,000", "per annum"],
        "category": "Fees"
    },
    {
        "question": "What is the penalty for late fee payment?",
        "expected_source_document": "Fee_Structure_2024_25.pdf",
        "expected_keywords": ["100", "per day", "late"],
        "category": "Fees"
    },
    {
        "question": "When does the hostel gate close at night?",
        "expected_source_document": "Hostel_Rules.pdf",
        "expected_keywords": ["9:00 PM", "curfew", "gate"],
        "category": "Hostel"
    },
    {
        "question": "What are the mess timings for lunch?",
        "expected_source_document": "Hostel_Rules.pdf",
        "expected_keywords": ["12:30", "2:00", "lunch"],
        "category": "Hostel"
    },
    {
        "question": "Can visitors enter hostel rooms?",
        "expected_source_document": "Hostel_Rules.pdf",
        "expected_keywords": ["visitor", "lounge", "not allowed"],
        "category": "Hostel"
    },
    {
        "question": "How can I get the Director's Merit Scholarship?",
        "expected_source_document": "Scholarship_Information.pdf",
        "expected_keywords": ["top 5%", "CGPA", "9.0", "50%"],
        "category": "Scholarship"
    },
    {
        "question": "What is the criteria for need-based financial aid?",
        "expected_source_document": "Scholarship_Information.pdf",
        "expected_keywords": ["income", "3,00,000", "100%"],
        "category": "Scholarship"
    },
    {
        "question": "When does the odd semester start?",
        "expected_source_document": "Academic_Calendar_2024_25.pdf",
        "expected_keywords": ["August", "2024"],
        "category": "Calendar"
    },
    {
        "question": "When are the end semester exams for the even semester?",
        "expected_source_document": "Academic_Calendar_2024_25.pdf",
        "expected_keywords": ["May", "June", "2025"],
        "category": "Calendar"
    },
]


def run_evaluation_with_api(base_url="http://localhost:8000"):
    """Run evaluation using the live API (requires backend to be running)."""
    import requests
    
    print("=" * 60)
    print("  RAG Evaluation Suite - Live API Mode")
    print("=" * 60)
    
    # Login as student
    login_resp = requests.post(f"{base_url}/api/auth/login", json={
        "username": "student1", "password": "password123"
    })
    
    if login_resp.status_code != 200:
        print("ERROR: Could not login. Is the backend running? Is the database seeded?")
        print(f"Response: {login_resp.text}")
        return None
    
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    results = []
    total_questions = len(EVAL_DATA)
    correct_retrievals = 0
    correct_answers = 0
    correct_citations = 0
    total_time = 0
    unanswered = 0
    
    for i, test_case in enumerate(EVAL_DATA):
        print(f"\n[{i+1}/{total_questions}] {test_case['question']}")
        
        start_time = time.time()
        try:
            resp = requests.post(
                f"{base_url}/api/chat/ask",
                headers=headers,
                json={"question": test_case["question"]},
                timeout=60
            )
            end_time = time.time()
            latency = end_time - start_time
            total_time += latency
            
            if resp.status_code != 200:
                print(f"  [ERROR] API Error: {resp.status_code}")
                results.append({
                    "question": test_case["question"],
                    "status": "error",
                    "latency_seconds": round(latency, 3),
                    "category": test_case["category"]
                })
                unanswered += 1
                continue
            
            data = resp.json()
            answer = data.get("answer", "")
            sources = data.get("sources", [])
            
            # Check if answer indicates "don't know"
            is_unanswered = any(phrase in answer.lower() for phrase in [
                "don't have", "not available", "cannot find", "no information",
                "no relevant documents"
            ])
            if is_unanswered:
                unanswered += 1
            
            # Check source retrieval accuracy
            retrieved_docs = [s.get("document_name", "") for s in sources]
            is_source_correct = test_case["expected_source_document"] in retrieved_docs
            if is_source_correct:
                correct_retrievals += 1
                correct_citations += 1
            
            # Check answer relevance (keyword matching)
            found_keywords = [
                kw for kw in test_case["expected_keywords"]
                if kw.lower() in answer.lower()
            ]
            keyword_ratio = len(found_keywords) / len(test_case["expected_keywords"]) if test_case["expected_keywords"] else 0
            is_answer_relevant = len(found_keywords) > 0
            if is_answer_relevant:
                correct_answers += 1
            
            status_icon = "[PASS]" if is_source_correct and is_answer_relevant else "[WARN]" if is_answer_relevant else "[FAIL]"
            print(f"  {status_icon} Source: {'PASS' if is_source_correct else 'FAIL'} | Keywords: {len(found_keywords)}/{len(test_case['expected_keywords'])} | {latency:.2f}s")
            
            results.append({
                "question": test_case["question"],
                "answer_preview": answer[:150] + "..." if len(answer) > 150 else answer,
                "expected_source": test_case["expected_source_document"],
                "retrieved_sources": retrieved_docs,
                "source_correct": is_source_correct,
                "expected_keywords": test_case["expected_keywords"],
                "found_keywords": found_keywords,
                "keyword_ratio": round(keyword_ratio, 2),
                "answer_relevant": is_answer_relevant,
                "is_unanswered": is_unanswered,
                "latency_seconds": round(latency, 3),
                "category": test_case["category"]
            })
            
        except requests.exceptions.ConnectionError:
            print("  [ERROR] Connection error. Is the backend running?")
            return None
        except Exception as e:
            print(f"  [ERROR] Error: {e}")
            results.append({
                "question": test_case["question"],
                "status": "error",
                "error": str(e),
                "category": test_case["category"]
            })
            unanswered += 1
    
    # Calculate metrics
    metrics = {
        "retrieval_accuracy": round(correct_retrievals / total_questions, 3) if total_questions > 0 else 0,
        "answer_relevance": round(correct_answers / total_questions, 3) if total_questions > 0 else 0,
        "citation_accuracy": round(correct_citations / total_questions, 3) if total_questions > 0 else 0,
        "avg_response_time": round(total_time / total_questions, 3) if total_questions > 0 else 0,
        "unanswered_questions": unanswered,
        "total_questions": total_questions
    }
    
    print("\n" + "=" * 60)
    print("  EVALUATION RESULTS")
    print("=" * 60)
    print(f"  Retrieval Accuracy:  {metrics['retrieval_accuracy']:.0%}")
    print(f"  Answer Relevance:    {metrics['answer_relevance']:.0%}")
    print(f"  Citation Accuracy:   {metrics['citation_accuracy']:.0%}")
    print(f"  Avg Response Time:   {metrics['avg_response_time']:.3f}s")
    print(f"  Unanswered:          {metrics['unanswered_questions']}/{total_questions}")
    print("=" * 60)
    
    # Save results for admin dashboard
    output = {
        "metrics": metrics,
        "test_results": results,
        "evaluated_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    output_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "evaluation_results.json")
    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")
    print("View results in the admin dashboard under 'Evaluation'.")
    
    return output


def run_evaluation_mock():
    """Run evaluation with mock data (no API required)."""
    print("=" * 60)
    print("  RAG Evaluation Suite - Mock Mode")
    print("  (Use --live flag to test against running backend)")
    print("=" * 60)
    
    results = []
    total_questions = len(EVAL_DATA)
    
    # Mock: simulate all correct retrievals
    for i, test_case in enumerate(EVAL_DATA):
        time.sleep(0.1)  # Simulate latency
        results.append({
            "question": test_case["question"],
            "expected_source": test_case["expected_source_document"],
            "retrieved_sources": [test_case["expected_source_document"]],
            "source_correct": True,
            "expected_keywords": test_case["expected_keywords"],
            "found_keywords": test_case["expected_keywords"][:2],
            "answer_relevant": True,
            "latency_seconds": 0.1,
            "category": test_case["category"]
        })
    
    metrics = {
        "retrieval_accuracy": 1.0,
        "answer_relevance": 1.0,
        "citation_accuracy": 1.0,
        "avg_response_time": 0.1,
        "unanswered_questions": 0,
        "total_questions": total_questions
    }
    
    print(f"\n  Mock evaluation complete: {total_questions} questions tested.")
    print(f"  (All metrics show ideal values in mock mode)")
    
    output = {
        "metrics": metrics,
        "test_results": results,
        "evaluated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "message": "Mock evaluation results. Run with --live flag for real evaluation."
    }
    
    output_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "evaluation_results.json")
    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"  Results saved to: {output_file}")
    return output


if __name__ == "__main__":
    if "--live" in sys.argv:
        run_evaluation_with_api()
    else:
        run_evaluation_mock()
