from django.shortcuts import render
from django.http import HttpResponse
from .models import Projects
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.core.files.storage import FileSystemStorage
import dropbox
import random, os
from .settings import dropbox_key
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

def index(request):
    #return HttpResponse("Hello world!")
    return render(request, "subforum/index.html")

def addNewProject(request):
    if request.method == 'POST':
        first_name = request.POST.get("fname")
        last_name = request.POST.get("lname")
        student_id = request.POST.get("student_id")
        email = request.POST.get("email")
        
        project_title = request.POST.get("title")
        url = request.POST.get("url")
        description = request.POST.get("message")
        uploaded_file = request.FILES['file']
        
        dbx = dropbox.Dropbox(os.getenv('DROPBOX_API_KEY'))
        
        try:
            
            dropbox_path = f'/Projects/{uploaded_file.name}-{random.randint(1, 100000000000000000)}'
            
            dbx.files_upload(uploaded_file.read(), dropbox_path)
            
            # Create a shared link for the uploaded file
            shared_link_metadata = dbx.sharing_create_shared_link_with_settings(dropbox_path)
            file_url = shared_link_metadata.url.replace("?dl=0", "?dl=1")  # Direct download link
            
            print(file_url)
            
            Projects.objects.create(
                first_name=first_name,
                last_name=last_name,
                student_id=student_id,
                email=email,
                title=project_title,
                url=url,
                description=description,
                file=file_url  # Save the file directly to Cloudinary
            )
            return render(request, "subforum/new_prjct.html", {
                    'success_message': 'Project submitted successfully!',
                })
        except IntegrityError as e:
                # Check the exact error type
                error_message = "An error occurred."
                if "student_id" in str(e):
                    error_message = "The Student ID is already in use."
                elif "email" in str(e):
                    error_message = "The Email is already in use."

                #return HttpResponseRedirect(f"{request.path}?error={error_message}")
                return render(request, "subforum/new_prjct.html", {
                    'first_name': first_name,
                    'last_name': last_name,
                    'student_id': student_id,
                    'email': email,
                    
                    'project_title': project_title,
                    'url': url,
                    'description': description,
                    'files': file_url,
                    'error_message': error_message,
                })

    return render(request, "subforum/new_prjct.html")