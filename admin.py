from django.contrib import admin
from .models import Comment, Company, Demand, Project, ProjectMember

admin.site.site_header = "Nexora · Administração"
admin.site.site_title = "Nexora"
admin.site.index_title = "Gestão do sistema"

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name", "active"]
    list_filter = ["active"]

class ProjectMemberInline(admin.TabularInline):
    model = ProjectMember
    extra = 0

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name", "company", "status"]
    list_filter = ["company", "status"]
    search_fields = ["name", "company__name"]
    inlines = [ProjectMemberInline]

@admin.register(Demand)
class DemandAdmin(admin.ModelAdmin):
    list_display = ["code", "title", "project", "priority", "status", "owner", "due_date"]
    list_filter = ["project__company", "project", "priority", "status"]
    search_fields = ["code", "title", "description"]
    readonly_fields = ["code", "created_by", "created_at", "updated_at"]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["demand", "author", "created_at"]
