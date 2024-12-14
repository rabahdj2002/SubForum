from django.db import models
from django.core.mail import send_mail
from django.utils.timezone import now

class Project(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Graded', 'Graded'),
    ]

    # Student Information
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    student_id = models.CharField(max_length=20, unique=True)  # Unique student identifier
    email = models.EmailField()  # Student's email for notifications

    # Project Information
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to=f'projects/')  # File upload for project
    submitted_at = models.DateTimeField(auto_now_add=True)

    # Grading Information
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')  # Grading status
    grade = models.CharField(max_length=5, blank=True, null=True)  # Grade (e.g., A+, 95)
    graded_at = models.DateTimeField(blank=True, null=True)  # When the project was graded
    grading_note = models.TextField(blank=True, null=True)  # Note or feedback from the teacher

    def __str__(self):
        return f"{self.student_id} - {self.title}"

    def mark_as_graded(self, grade_value, note=None):
        """
        Marks the project as graded, sets the grade, adds a grading note, updates the timestamp,
        and sends an email notification.
        """
        self.status = 'Graded'
        self.grade = grade_value
        self.grading_note = note
        self.graded_at = now()
        self.save()

        # Send email notification to the student
        subject = "Your project has been graded!"
        message = (
            f"Hello {self.first_name} {self.last_name},\n\n"
            f"Your project '{self.title}' has been graded.\n"
            f"Status: {self.status}\n"
            f"Grade: {self.grade}\n"
            f"Teacher's Note: {self.grading_note or 'No additional notes provided.'}\n\n"
            f"Check with your teacher or the website for more details.\n\n"
            "Best regards,\n"
            "Your Teacher"
        )
        send_mail(subject, message, 'teacher@example.com', [self.email])

    def is_graded(self):
        """
        Returns True if the project has been graded.
        """
        return self.status == 'Graded'
