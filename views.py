from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import DemandForm
from .models import Demand, Project

class NexoraLoginView(LoginView):
    template_name = "core/login.html"
    redirect_authenticated_user = True

@login_required
def dashboard(request):
    projects = Project.objects.filter(status="active")
    if not request.user.is_staff:
        projects = projects.filter(members=request.user)
    demands = Demand.objects.filter(project__in=projects).select_related("project__company", "owner")
    context = {
        "total": demands.exclude(status__in=[Demand.Status.DONE, Demand.Status.CANCELED]).count(),
        "progress": demands.filter(status=Demand.Status.PROGRESS).count(),
        "testing": demands.filter(status=Demand.Status.TEST).count(),
        "done": demands.filter(status=Demand.Status.DONE).count(),
        "recent": demands[:6],
        "projects": projects,
        "companies": sorted({p.company for p in projects}, key=lambda c: c.name),
        "status_counts": demands.values("status").annotate(count=Count("id")),
    }
    return render(request, "core/dashboard.html", context)

@login_required
def demand_list(request):
    projects = Project.objects.filter(status="active")
    if not request.user.is_staff:
        projects = projects.filter(members=request.user)
    query = request.GET.get("q", "").strip()
    demands = Demand.objects.filter(project__in=projects).select_related("project__company", "owner")
    if query:
        demands = demands.filter(Q(code__icontains=query) | Q(title__icontains=query) | Q(description__icontains=query))
    return render(request, "core/demands.html", {"demands": demands, "query": query})

@login_required
def demand_create(request):
    if request.method == "POST":
        form = DemandForm(request.POST, user=request.user)
        if form.is_valid():
            demand = form.save(commit=False)
            demand.created_by = request.user
            if not request.user.is_staff and not demand.project.members.filter(pk=request.user.pk).exists():
                messages.error(request, "Você não tem acesso a esse sistema.")
                return redirect("demands")
            demand.save()
            messages.success(request, f"A demanda {demand.code} foi criada.")
            return redirect("dashboard")
    else:
        form = DemandForm(user=request.user)
    return render(request, "core/demand_form.html", {"form": form})

@login_required
@require_POST
def demand_delete(request, pk):
    demand = get_object_or_404(Demand.objects.select_related("project"), pk=pk)
    if not request.user.is_staff and not demand.project.members.filter(pk=request.user.pk).exists():
        messages.error(request, "Você não tem acesso a essa demanda.")
        return redirect("demands")
    demand.delete()
    messages.success(request, "Demanda removida.")
    return redirect("demands")
