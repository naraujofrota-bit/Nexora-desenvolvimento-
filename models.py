from django.conf import settings
from django.db import models

class Company(models.Model):
    name = models.CharField("nome", max_length=140, unique=True)
    active = models.BooleanField("ativa", default=True)
    created_at = models.DateTimeField("criada em", auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "empresa"
        verbose_name_plural = "empresas"

    def __str__(self):
        return self.name

class Project(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Ativo"
        PAUSED = "paused", "Pausado"
        CLOSED = "closed", "Encerrado"

    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="projects", verbose_name="empresa")
    name = models.CharField("nome do sistema", max_length=160)
    description = models.TextField("descrição", blank=True)
    status = models.CharField("situação", max_length=12, choices=Status.choices, default=Status.ACTIVE)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through="ProjectMember", related_name="nexora_projects", blank=True)

    class Meta:
        ordering = ["company__name", "name"]
        verbose_name = "sistema"
        verbose_name_plural = "sistemas"
        constraints = [models.UniqueConstraint(fields=["company", "name"], name="unique_project_per_company")]

    def __str__(self):
        return f"{self.company} · {self.name}"

class ProjectMember(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "project"], name="unique_project_member")]

class Demand(models.Model):
    class Kind(models.TextChoices):
        BUG = "bug", "Bug/erro"
        FIX = "fix", "Correção"
        IMPROVEMENT = "improvement", "Melhoria"
        FEATURE = "feature", "Nova funcionalidade"
        TECHNICAL = "technical", "Tarefa técnica"
        VISUAL = "visual", "Ajuste visual"

    class Priority(models.TextChoices):
        CRITICAL = "critical", "Crítica"
        HIGH = "high", "Alta"
        MEDIUM = "medium", "Média"
        LOW = "low", "Baixa"

    class Status(models.TextChoices):
        TODO = "todo", "A fazer"
        PROGRESS = "progress", "Em andamento"
        TEST = "test", "Em teste"
        DONE = "done", "Concluída"
        CANCELED = "canceled", "Cancelada"

    code = models.CharField("código", max_length=20, unique=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name="demands", verbose_name="sistema")
    title = models.CharField("título", max_length=180)
    description = models.TextField("descrição", blank=True)
    kind = models.CharField("tipo", max_length=20, choices=Kind.choices, default=Kind.FIX)
    priority = models.CharField("prioridade", max_length=12, choices=Priority.choices, default=Priority.MEDIUM)
    status = models.CharField("situação", max_length=12, choices=Status.choices, default=Status.TODO)
    blocked = models.BooleanField("bloqueada", default=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_demands", verbose_name="responsável")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="created_demands", verbose_name="criada por")
    due_date = models.DateField("prazo", null=True, blank=True)
    created_at = models.DateTimeField("criada em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizada em", auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "demanda"
        verbose_name_plural = "demandas"

    def save(self, *args, **kwargs):
        if not self.code:
            latest = Demand.objects.order_by("-id").values_list("id", flat=True).first() or 0
            self.code = f"NX-{latest + 201:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} · {self.title}"

class Comment(models.Model):
    demand = models.ForeignKey(Demand, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
