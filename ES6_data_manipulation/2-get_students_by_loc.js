// Returns an array of objects who are located in a specific city.
const getStudentsByLocation = (students, city) => {
    const studentsLocation = students.filter(
      (student) => student.location === city,
    );
  
    return studentsLocation;
  };
  
  export default getStudentsByLocation;