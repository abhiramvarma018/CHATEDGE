from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_sgpa(grades, credits):
    total_points = sum(grades[i] * credits[i] for i in range(len(grades)))
    total_credits = sum(credits)

    if total_credits == 0:
        return 0  # Return 0 if total credits are zero

    sgpa = total_points / total_credits
    return sgpa

def calculate_cgpa(sgpa_list, credits_list):
    total_points = sum(sgpa_list[i] * credits_list[i] for i in range(min(len(sgpa_list), len(credits_list))))
    total_credits = sum(credits_list)

    if total_credits == 0:
        return 0  # Return 0 if total credits are zero

    cgpa = total_points / total_credits
    return cgpa

def cgpa_to_percentage(cgpa):
    percentage_equivalence = (cgpa - 0.5) * 10
    return percentage_equivalence

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        num_semesters = int(request.form['num_semesters'])

        all_sgpa = []
        all_credits = []

        for semester in range(1, num_semesters + 1):
            semester_grades = list(map(int, request.form.getlist(f'semester{semester}_grades[]')))
            semester_credits = list(map(int, request.form.getlist(f'semester{semester}_credits[]')))

            sgpa = calculate_sgpa(semester_grades, semester_credits)
            all_sgpa.append(sgpa)
            all_credits.extend(semester_credits)

        print("All SGPA:", all_sgpa)
        print("All Credits:", all_credits)

        cgpa = calculate_cgpa(all_sgpa, all_credits)
        percentage_equivalence = cgpa_to_percentage(cgpa)

        print("CGPA:", cgpa)
        print("Percentage Equivalence:", percentage_equivalence)

        return render_template('result.html', cgpa=cgpa, percentage_equivalence=percentage_equivalence, semester_sgpa=all_sgpa, num_semesters=num_semesters)

    return render_template('gpa.html')

if __name__ == '__main__':
    app.run(debug=True)
