import os
from fpdf import FPDF

# Ensure the output directory exists
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "documents")
os.makedirs(OUTPUT_DIR, exist_ok=True)

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 15)
        self.cell(0, 10, "Rajiv Gandhi Institute of Technology (RGIT)", border=False, ln=True, align="C")
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.5)
        self.line(10, 22, 200, 22)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def generate_pdf(filename, title, sections):
    pdf = PDF()
    pdf.add_page()
    
    # Document Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, title, ln=True, align="C")
    pdf.ln(10)
    
    for section_title, content in sections.items():
        # Section Heading
        pdf.set_font("Arial", "B", 12)
        pdf.set_fill_color(220, 220, 220)
        pdf.cell(0, 10, section_title, ln=True, fill=True)
        pdf.ln(2)
        
        # Section Content
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 6, content)
        pdf.ln(5)
    
    filepath = os.path.join(OUTPUT_DIR, filename)
    pdf.output(filepath)
    print(f"Generated {filepath}")

def generate_all():
    print("Generating sample PDFs...")
    
    # 1. Attendance Regulations
    generate_pdf(
        "Attendance_Regulations.pdf",
        "Attendance Regulations and Guidelines",
        {
            "1. Minimum Attendance Requirement": "The minimum attendance requirement for all undergraduate and postgraduate courses is 75% in each subject. Students must attend lectures, tutorials, and practical sessions regularly. Attendance is calculated from the date of commencement of classes as per the academic calendar.",
            "2. Medical Leave Provisions": "Students falling sick must inform the Head of the Department immediately. A medical certificate from a registered medical practitioner must be submitted within three days of joining back. However, medical leave does not automatically waive the attendance requirement.",
            "3. Attendance Shortage Consequences": "Students with attendance less than 75% in a subject will not be permitted to appear for the end-semester examination in that subject. They will be marked as 'Detained' and must repeat the course when offered next.",
            "4. Condonation Rules": "In exceptional cases (medical emergency, participation in national-level sports/cultural events), a maximum condonation of 10% (i.e., attendance between 65% and 74%) may be granted by the Principal upon recommendation by the HOD. A condonation fee of Rs. 1000/- is applicable.",
            "5. Attendance Recording Procedures": "Faculty members will record attendance using the biometric system or ERP portal within the first 10 minutes of the class. Students are advised to verify their attendance status on the student portal weekly."
        }
    )

    # 2. Examination Rules
    generate_pdf(
        "Examination_Rules.pdf",
        "Rules and Regulations for Examinations",
        {
            "1. Exam Eligibility Criteria": "To be eligible for end-semester exams, a student must: (a) Have minimum 75% attendance. (b) Have cleared all fee dues. (c) Have satisfactorily completed all internal assessments and assignments.",
            "2. Internal vs External Marking": "The evaluation consists of 40% Continuous Internal Assessment (CIA) and 60% End Semester Examination (ESE). CIA includes mid-term tests, assignments, and attendance. ESE is a 3-hour written examination.",
            "3. Grade System": "The institute follows a 10-point grading system: O (Outstanding, 10 points, 90-100 marks), A+ (Excellent, 9 points, 80-89 marks), A (Very Good, 8 points, 70-79 marks), B+ (Good, 7 points, 60-69 marks), B (Above Average, 6 points, 50-59 marks), C (Average, 5 points, 40-49 marks), F (Fail, 0 points, <40 marks).",
            "4. CGPA Calculation": "Semester Grade Point Average (SGPA) is calculated as Sum(Credits * Grade Points) / Sum(Credits) for a semester. Cumulative Grade Point Average (CGPA) is similarly calculated for all completed semesters.",
            "5. Re-examination Rules": "Students failing in a subject (F grade) must appear for the supplementary examination held before the next academic year. The internal marks will be carried forward.",
            "6. Malpractice Penalties": "Any student found copying or using unfair means during exams will face strict disciplinary action, which may include cancellation of the entire semester's exams or expulsion from the college.",
            "7. Question Paper Pattern": "The end-semester question paper typically consists of Part A (10 short questions of 2 marks each) and Part B (5 long questions of 16 marks each, with internal choice)."
        }
    )

    # 3. Fee Structure
    generate_pdf(
        "Fee_Structure_2024_25.pdf",
        "Fee Structure for Academic Year 2024-25",
        {
            "1. Tuition Fees": "- B.Tech (Computer Science, IT): Rs. 1,20,000 per annum\n- B.Tech (Electronics, Mechanical, Civil): Rs. 1,10,000 per annum\n- M.Tech (All specializations): Rs. 90,000 per annum",
            "2. Hostel Fees": "- Single Seater AC: Rs. 80,000 per annum\n- Double Seater Non-AC: Rs. 60,000 per annum\n- Mess Charges: Rs. 40,000 per annum (mandatory for hostellers)",
            "3. Library and Lab Fees": "An annual library and laboratory fee of Rs. 10,000 is applicable to all students.",
            "4. Examination Fees": "Examination fees of Rs. 2,000 per semester must be paid before filling the exam form. Supplementary exam fee is Rs. 500 per subject.",
            "5. Late Payment Penalties": "Fees must be paid before the start of the semester. A late fine of Rs. 100 per day is charged for the first 15 days, after which the student's name may be struck off the rolls.",
            "6. Payment Methods": "Fees can be paid online via the student ERP portal using Net Banking, UPI, or Credit/Debit Card. Demand Drafts in favor of 'RGIT' payable at the city branch are also accepted. Cash payments are strictly not accepted."
        }
    )

    # 4. Hostel Rules
    generate_pdf(
        "Hostel_Rules.pdf",
        "Hostel Rules and Regulations",
        {
            "1. Room Allotment Procedure": "Rooms are allotted on a first-come, first-served basis, prioritizing outstation students. Mutual exchange of rooms is strictly prohibited without written permission from the Warden.",
            "2. Timings and Curfew": "The hostel gates close at 9:00 PM (8:00 PM for first-year students). Late entry requires prior written permission from the Warden and a valid reason.",
            "3. Visitor Policy": "Visitors are allowed only in the designated visitor's lounge between 4:00 PM and 6:00 PM on weekdays, and 10:00 AM to 6:00 PM on weekends. No visitor is allowed inside student rooms.",
            "4. Mess Rules and Timings": "Breakfast: 7:30 AM - 8:45 AM, Lunch: 12:30 PM - 2:00 PM, Snacks: 5:00 PM - 6:00 PM, Dinner: 7:30 PM - 9:00 PM. Food must be consumed in the dining hall only.",
            "5. Disciplinary Actions": "Possession or consumption of alcohol, drugs, or tobacco products is strictly banned and will lead to immediate expulsion from the hostel. Ragging is a criminal offense.",
            "6. Leave Procedures": "Students planning to stay out overnight or go home must fill out the out-pass form online and get it approved by the Warden and Local Guardian/Parents."
        }
    )

    # 5. Scholarship Information
    generate_pdf(
        "Scholarship_Information.pdf",
        "Scholarships and Financial Aid",
        {
            "1. Merit Scholarships": "The 'Director's Merit Scholarship' is awarded to the top 5% of students in each branch based on CGPA (minimum 9.0 required). It provides a 50% waiver on tuition fees for the next academic year.",
            "2. Need-based Scholarships": "Students with an annual family income of less than Rs. 3,00,000 are eligible for the 'RGIT Financial Aid'. It covers up to 100% of tuition fees, subject to maintaining a CGPA of 7.5.",
            "3. Government Scholarships": "The college facilitates various state and central government scholarships for SC/ST, OBC, and minority category students. Students must apply through the National Scholarship Portal (NSP).",
            "4. Application Procedure": "Applications for college scholarships open in August every year. Students must submit the application form along with income certificates and mark sheets to the Scholarship Section.",
            "5. Important Dates": "Scholarship portal opens: August 15. Last date to apply: September 30. Announcement of awardees: November 15."
        }
    )

    # 6. Academic Calendar
    generate_pdf(
        "Academic_Calendar_2024_25.pdf",
        "Academic Calendar 2024-25",
        {
            "1. Odd Semester Dates": "Commencement of Classes: August 1, 2024. Mid-Term Exams: October 7-12, 2024. Last working day: November 30, 2024. End Semester Exams: December 5-24, 2024.",
            "2. Even Semester Dates": "Commencement of Classes: January 15, 2025. Mid-Term Exams: March 17-22, 2025. Last working day: May 15, 2025. End Semester Exams: May 20 - June 10, 2025.",
            "3. Holidays": "Independence Day: Aug 15. Gandhi Jayanti: Oct 2. Diwali: Oct 29-Nov 3. Christmas: Dec 25. Republic Day: Jan 26. Holi: Mar 14.",
            "4. Registration Deadlines": "Odd Semester Registration: July 15-25, 2024. Even Semester Registration: Jan 2-10, 2025. Late registration incurs a fine.",
            "5. Important Events": "Tech Fest: October 20-22, 2024. Cultural Fest (Tarang): February 20-22, 2025. Sports Meet: March 15-18, 2025. Convocation: July 25, 2025."
        }
    )

if __name__ == "__main__":
    generate_all()
