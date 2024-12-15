from django.shortcuts import render
from django.http import HttpResponse
from .models import Projects
from cloudinary.uploader import upload
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.core.files.storage import FileSystemStorage


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
        files = request.FILES.getlist('file')  # Get list of uploaded files
        file_urls = []
        
        # Save the file using FileSystemStorage
        #fs = FileSystemStorage()
        #filename = fs.save(uploaded_file.name, uploaded_file)
        #file_url = fs.url(filename)
        
        try:
            for file in files:
                upload_response = upload(file, resource_type="auto")  # Upload file to Cloudinary
                file_urls.append(upload_response['url'])  # Get file URL
                
            # Save the project object
            project = Projects.objects.create(
                first_name=first_name,
                last_name=last_name,
                student_id=student_id,
                email=email,
                title=project_title,
                url=url,
                description=description,
                file=file_urls  # Save the file directly to Cloudinary
            )
            
            
            
            

            # Save each uploaded file
            #for file in files:
            #    project.files.save(file.name, file, save=True)

            return JsonResponse({"success": True, "message": "Project submitted successfully!"})
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
                    'files': files,
                    'error_message': error_message,
                })

    return render(request, "subforum/new_prjct.html")