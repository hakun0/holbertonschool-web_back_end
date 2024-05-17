export default function updateStudentGradeByCity(students, city, grades) {
    return students.filter((student) => student.location === city)
      .map((student) => {
        const ok = grades.find((grade) => grade.studentId === student.id);
        return { ...student, grade: ok ? ok.grade : 'N/A' };
      });
  }