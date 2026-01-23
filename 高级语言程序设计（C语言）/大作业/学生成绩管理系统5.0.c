
#include <stdio.h>
#include <string.h>
#define MAX_STUDENTS 30
#define MAX_SUBJECTS 6

typedef struct {//定义结构体类型 
    char id[15];
    char name[30];
    float grades[MAX_SUBJECTS];
    float total;
    float average;
} Student;

void InputStudentRecords(Student students[], int studentCount, int subjectCount);// 输入每个学生的学号、姓名、各科成绩
void CalculateTotalAndAverageForCourses(Student students[], int studentCount, int subjectCount); // 计算每门课程的总分和平均分
void CalculateTotalAndAverageForStudents(Student students[], int studentCount, int subjectCount);   // 计算每个学生的总分和平均分(包输出)
void CalculateTotalAndAverageForStudentsNo(Student students[], int studentCount, int subjectCount);//计算每个学生的总分和平均分(不包输出)
void SortStudentsByTotalScoreDesc(Student students[], int studentCount);// 按每个学生的总分由高到低排名
void SortStudentsByTotalScoreAsc(Student students[], int studentCount);// 按每个学生的总分由低到高排名
void SortStudentsByID(Student students[], int studentCount);// 按学号排序
void SortStudentsByName(Student students[], int studentCount) ;// 按姓名的字典顺序排序
void PrintStudents(const Student students[], int studentCount, int subjectCount);//打印表格 
void SearchStudentByID(Student students[], int studentCount,int subjectCount, const char* id);// 按学号查询学生排名及其各科成绩
void SearchStudentByName(Student students[], int studentCount,int subjectCount,const char* name);// 按姓名查询学生排名及其各科成绩
void PerformStatisticalAnalysis(Student students[], int studentCount,int subjectCount);// 统计分析
void ListAllRecords(Student students[], int studentCount, int subjectCount);// 列出所有记录，包括课程总分和平均分
//主函数 
int main()
{
    Student students[MAX_STUDENTS]; // 存储学生记录的数组
    int studentCount = 0;           // 实际学生数量
    int subjectCount = 0;          // 实际科目数量         
    char searchID[15],searchName[30];//被查询的学号及名字 
    printf("Enter the number of students (max %d): ", MAX_STUDENTS);
    scanf("%d", &studentCount);

    printf("Enter the number of subjects (max %d): ", MAX_SUBJECTS);
    scanf("%d", &subjectCount);

    // 确保输入的学生和课程数量是有效的
    studentCount = (studentCount > 0 && studentCount <= MAX_STUDENTS) ? studentCount : MAX_STUDENTS;
    subjectCount = (subjectCount > 0 && subjectCount <= MAX_SUBJECTS) ? subjectCount : MAX_SUBJECTS;

    int choice;
    do {
        // 显示菜单...
        printf("*---------------------------------------------*\n");
        printf("1. Input record\n");
        printf("2. Calculate total and average score of every course\n");
        printf("3. Calculate total and average score of every student\n");
        printf("4. Sort in descending order by total score of every student\n");
        printf("5. Sort in ascending order by total score of every student\n");
        printf("6. Sort in ascending order by number\n");
        printf("7. Sort in dictionary order by name\n");
        printf("8. Search by number\n");
        printf("9. Search by name\n");
        printf("10. Statistic analysis\n");
        printf("11. List record\n");
        printf("0. Exit\n");
        printf("Please enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                InputStudentRecords(students, studentCount, subjectCount);
                break;
            case 2:
                CalculateTotalAndAverageForCourses(students, studentCount, subjectCount);
                break;
            case 3:
                CalculateTotalAndAverageForStudents(students, studentCount, subjectCount);
                break;
            case 4:
            	CalculateTotalAndAverageForStudentsNo(students, studentCount, subjectCount);
                SortStudentsByTotalScoreDesc(students, studentCount);
                printf("Students sorted by total score (descending):\n");
                PrintStudents(students, studentCount, subjectCount);
                break;
            case 5:
            	CalculateTotalAndAverageForStudentsNo(students, studentCount, subjectCount);
                SortStudentsByTotalScoreAsc(students, studentCount);
                printf("Students sorted by total score (ascending):\n");
                PrintStudents(students, studentCount, subjectCount);
                break;
            case 6:
            	CalculateTotalAndAverageForStudentsNo(students, studentCount, subjectCount);
                SortStudentsByID(students, studentCount);
                printf("Students sorted by ID:\n");
                PrintStudents(students, studentCount, subjectCount);
                break;
            case 7:
            	CalculateTotalAndAverageForStudentsNo(students, studentCount, subjectCount);
                SortStudentsByName(students, studentCount);
                printf("Students sorted by name:\n");
                PrintStudents(students, studentCount, subjectCount);
                break;
            case 8:
                printf("Enter the student ID you want to search:");
                scanf(" %s",searchID);
                SearchStudentByID(students, studentCount,subjectCount, searchID);
                break;
            case 9:
            	printf("Enter the student name you want to search:");
                scanf(" %s",searchName);
                SearchStudentByName(students, studentCount, subjectCount,searchName);
                break;
            case 10:
                PerformStatisticalAnalysis(students, studentCount,subjectCount);
                break;
            case 11:
                ListAllRecords(students, studentCount, subjectCount);
                break;
            case 0:
                printf("Exiting program...\n");
                break;
            default:
                printf("Invalid choice. Please try again.\n");
        }
    } while (choice != 0);

    return 0;
}
// 输入每个学生的学号、姓名、各科成绩
void InputStudentRecords(Student students[], int studentCount, int subjectCount) {
	int i,j;
    for ( i = 0; i < studentCount; i++) {
        printf("Enter information for student %d:\n", i + 1);
        printf("ID: ");
        scanf("%s", students[i].id);
        printf("Name: ");
        scanf("%s", students[i].name);
        for ( j = 0; j < subjectCount; j++) {
            printf("Subject %d score: ", j + 1);
            scanf("%f", &students[i].grades[j]);
        }
    }
}
// 计算每门课程的总分和平均分
void CalculateTotalAndAverageForCourses(Student students[], int studentCount, int subjectCount) {
	int i,j;
    for ( i = 0; i < subjectCount; i++) {
        float total = 0.0;
        for ( j = 0; j < studentCount; j++) {
            total += students[j].grades[i];
        }
        float average = total / studentCount;
        printf("Subject %d -> Total: %.2f, Average: %.2f\n", i + 1, total, average);
    }
}

// 计算每个学生的总分和平均分(包括输出) 
void CalculateTotalAndAverageForStudents(Student students[], int studentCount, int subjectCount) {
	int i,j;
    for ( i = 0; i < studentCount; i++) {
        students[i].total = 0.0;
        for ( j = 0; j < subjectCount; j++) {
            students[i].total += students[i].grades[j];
        }
        students[i].average = students[i].total / subjectCount;
        printf("Student %d ->Total: %.2f ,Average: %.2f \n",i+1,students[i].total, students[i].average);
    }
}
//计算每个学生的总分和平均分(不包括输出，给排序用) 
void CalculateTotalAndAverageForStudentsNo(Student students[], int studentCount, int subjectCount) {
	int i,j;
    for ( i = 0; i < studentCount; i++) {
        students[i].total = 0.0;
        for ( j = 0; j < subjectCount; j++) {
            students[i].total += students[i].grades[j];
        }
        students[i].average = students[i].total / subjectCount;
    }
}
// 按每个学生的总分由高到低排出名次表
void SortStudentsByTotalScoreDesc(Student students[], int studentCount) {
    // 冒泡排序，按总成绩降序
    int i,j;
    for ( i = 0; i < studentCount - 1; ++i) {
        for ( j = 0; j < studentCount - 1 - i; ++j) {
            if (students[j].total < students[j + 1].total) {
                Student temp = students[j];
                students[j] = students[j + 1];
                students[j + 1] = temp;
            }
        }
    }
}

// 按每个学生的总分由低到高排出名次表
void SortStudentsByTotalScoreAsc(Student students[], int studentCount) {
    // 冒泡排序，按总成绩升序
    int i,j;
    for ( i = 0; i < studentCount - 1; ++i) {
        for (j = 0; j < studentCount - 1 - i; ++j) {
            if (students[j].total > students[j + 1].total) {
                Student temp = students[j];
                students[j] = students[j + 1];
                students[j + 1] = temp;
            }
        }
    }
}

// 按学号由小到大排出成绩表
void SortStudentsByID(Student students[], int studentCount) {
    // 冒泡排序，按学号升序
    int i,j;
    for ( i = 0; i < studentCount - 1; ++i) {
        for ( j = 0; j < studentCount - 1 - i; ++j) {
            if (strcmp(students[j].id, students[j + 1].id) > 0) {
                Student temp = students[j];
                students[j] = students[j + 1];
                students[j + 1] = temp;
            }
        }
    }
}

// 按姓名的字典顺序排出成绩表
void SortStudentsByName(Student students[], int studentCount) {
    // 冒泡排序，按姓名字典顺序
    int i,j;
    for ( i = 0; i < studentCount - 1; ++i) {
        for ( j = 0; j < studentCount - 1 - i; ++j) {
            if (strcmp(students[j].name, students[j + 1].name) > 0) {
                Student temp = students[j];
                students[j] = students[j + 1];
                students[j + 1] = temp;
            }
        }
    }
}
// 打印学生记录的表格
void PrintStudents(const Student students[], int studentCount, int subjectCount) {
	int i,j;
    printf("+Rank-+-----ID--------+---------Name-----------------+");
    for ( i = 0; i < subjectCount; ++i) {
        printf(" Sub%02d |", i + 1);
    }
    printf(" Total  | Average |\n");
    // 打印分割线
    printf("+-----+---------------+------------------------------+");
    for ( i = 0; i < subjectCount; ++i) {
        printf("-------+");
    }
    printf("--------+---------+\n");
    
    for ( i = 0; i < studentCount; ++i) {
        printf("| %-3d | %-13s | %-28s |", i + 1, students[i].id, students[i].name);
        for ( j = 0; j < subjectCount; ++j) {
            printf(" %-5.2f |", students[i].grades[j]);
        }
        printf(" %-5.2f | %-7.2f |\n", students[i].total, students[i].average);
    }
    // 打印结束分割线
    printf("+-----+---------------+------------------------------+");
    for ( i = 0; i < subjectCount; ++i) {
        printf("-------+");
    }
    printf("--------+---------+\n");
}
// 按学号查询学生排名及其各科考试成绩 
void SearchStudentByID(Student students[], int studentCount,int subjectCount, const char* id) {
	int i,j,k; 
    for ( i = 0; i < studentCount; ++i) {
        if (strcmp(students[i].id, id) == 0) {
            // 计算排名
            int rank = 1;
            for ( j = 0; j < studentCount; ++j) {
                if (students[j].total > students[i].total) {
                    rank++;
                }
            }
            // 打印学生信息和排名
            printf("Student found: ID: %s, Name: %s, Rank: %d\n", students[i].id, students[i].name, rank);
            printf("Grades:");
            for ( k = 0; k < subjectCount; ++k) {
                printf(" %.2f", students[i].grades[k]);
            }
            printf("\n");
            return; // 退出函数，因为已找到学生
        }
    }
    printf("Student with ID %s not found.\n", id);
}
// 按姓名查询学生排名及其各科考试成绩
void SearchStudentByName(Student students[], int studentCount,int subjectCount, const char* name) {
	int i,j,k;
    for (i = 0; i < studentCount; ++i) {
        if (strcmp(students[i].name, name) == 0) {
            // 计算排名
            int rank = 1;
            for (j = 0; j < studentCount; ++j) {
                if (students[j].total > students[i].total) {
                    rank++;
                }
            }
            // 打印学生信息和排名
            printf("Student found: Name: %s, ID: %s, Rank: %d\n", students[i].name, students[i].id, rank);
            printf("Grades:");
            for (k = 0; k < subjectCount; ++k) {
                printf(" %.2f", students[i].grades[k]);
            }
            printf("\n");
            return; // 退出函数，因为已找到学生
        }
    }
    printf("Student with name %s not found.\n", name);
}
//按优秀（90-100）、良好（80-89）、中等（70-79）、及格（60-69）、不及格（0-59）5个类别，统计每个类别的人数以及所占的百分比；
void PerformStatisticalAnalysis(Student students[], int studentCount, int subjectCount) {
    int i, j; 
    int gradeDistribution[5] = {0};
    for (i = 0; i < studentCount; ++i) {
        float sum = 0.0;
        for (j = 0; j < subjectCount; ++j) {
            sum += students[i].grades[j];
        }
        float average = sum / subjectCount;
        if (average >= 90.0)
            gradeDistribution[0] += 1;
        else if (average >= 80.0)
            gradeDistribution[1] += 1;
        else if (average >= 70.0)
            gradeDistribution[2] += 1;
        else if (average >= 60.0)
            gradeDistribution[3] += 1;
        else
            gradeDistribution[4] += 1;
    }

    // 输出统计信息
    const char *categories[] = {"Excellent", "Good", "Average", "Pass", "Fail"};
    int totalGrades = studentCount;
    printf("Grade distribution:\n");
    for (i = 0; i < 5; ++i) {
        float percentage = (gradeDistribution[i] / (float)totalGrades) * 100;
        printf("%s: %d (%.2f%%)\n", categories[i], gradeDistribution[i], percentage);
    }
}
//输出每个学生的学号、姓名、各科考试成绩、总分、平均分，以及每门课程的总分和平均分。
void ListAllRecords(Student students[], int studentCount, int subjectCount) {
	int i,j;
    float subjectTotals[MAX_SUBJECTS] = {0.0};
    for (i = 0; i < studentCount; ++i) {
        students[i].total = 0.0;
        for ( j = 0; j < subjectCount; ++j) {
            students[i].total += students[i].grades[j];
            subjectTotals[j] += students[i].grades[j];
        }
        students[i].average = students[i].total / (float)subjectCount;
    }

    // 打印学生数据
    printf("Student records:\n");
    for (i = 0; i < studentCount; ++i) {
        printf("ID: %s, Name: %s, Total: %.2f, Average: %.2f\n", students[i].id, students[i].name, students[i].total, students[i].average);
        printf("Grades: ");
        for (j = 0; j < subjectCount; ++j) {
            printf("%.2f ", students[i].grades[j]);
        }
        printf("\n");
    }

    // 打印每个科目的总分和平均分
    printf("Subject totals and averages:\n");
    for ( i = 0; i < subjectCount; ++i) {
        float subjectAverage = subjectTotals[i] / (float)studentCount;
        printf("Subject %d: Total: %.2f, Average: %.2f\n", i + 1, subjectTotals[i], subjectAverage);
    }
}

