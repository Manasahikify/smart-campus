from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count
from django.http import HttpResponse

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from .models import Report
from .forms import ReportForm


# ✅ WELCOME PAGE
def welcome(request):
    return render(request, 'welcome.html')


# ✅ HOME PAGE
@login_required
def home(request):
    reports = Report.objects.all()
    return render(request, 'home.html', {'reports': reports})


# ✅ SUBMIT REPORT
@login_required
def report_issue(request):

    if request.method == "POST":
        form = ReportForm(request.POST, request.FILES)

        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.save()

            messages.success(request, "Report submitted successfully!")

            return redirect('home')

    else:
        form = ReportForm()

    return render(request, 'report.html', {'form': form})


# ✅ ADMIN DASHBOARD
@staff_member_required
def admin_dashboard(request):

    reports = Report.objects.all()

    # 📊 COUNTS
    total = reports.count()
    pending = reports.filter(status="Reported").count()
    in_progress = reports.filter(status="In Progress").count()
    resolved = reports.filter(status="Resolved").count()

    # 📈 PIE CHART DATA
    type_counts = Report.objects.values('report_type').annotate(count=Count('id'))

    labels = [item['report_type'] for item in type_counts]
    data = [item['count'] for item in type_counts]

    # 🔁 STATUS UPDATE + REPLY
    if request.method == "POST":

        report_id = request.POST.get("report_id")
        report = Report.objects.get(id=report_id)

        # ✅ STATUS UPDATE
        new_status = request.POST.get("status")

        if new_status:

            report.status = new_status
            report.save()

            # ✅ SEND EMAIL TO USER
            if report.user.email:

                send_mail(
                    subject="Smart Campus Status Update",

                    message=f"""
Hello {report.user.username},

Your report status has been updated.

Report Type: {report.report_type}
Location: {report.location}

New Status: {new_status}

Thank you,
Smart Campus Team
""",

                    from_email=settings.EMAIL_HOST_USER,

                    recipient_list=[report.user.email],

                    fail_silently=False
                )

            messages.success(request, "Status updated & email sent!")

        # ✅ ADMIN REPLY
        reply = request.POST.get("admin_reply")

        if reply:

            report.admin_reply = reply
            report.save()

            # ✅ SEND REPLY EMAIL
            if report.user.email:

                send_mail(
                    subject="Reply From Smart Campus Admin",

                    message=f"""
Hello {report.user.username},

Admin replied to your report.

Reply:
{reply}

Thank you,
Smart Campus Team
""",

                    from_email=settings.EMAIL_HOST_USER,

                    recipient_list=[report.user.email],

                    fail_silently=False
                )

            messages.success(request, "Reply sent successfully!")

    return render(request, 'dashboard.html', {

        'reports': reports,
        'total': total,
        'pending': pending,
        'in_progress': in_progress,
        'resolved': resolved,
        'labels': labels,
        'data': data

    })


# ✅ USER REPORTS
@login_required
def my_reports(request):

    reports = Report.objects.filter(user=request.user)

    return render(request, 'my_reports.html', {

        'reports': reports

    })


# ✅ REPORT DETAILS
@login_required
def report_detail(request, pk):

    report = get_object_or_404(Report, pk=pk)

    return render(request, 'report_detail.html', {

        'report': report

    })


# ✅ EXPORT PDF
@staff_member_required
def export_pdf(request):

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'attachment; filename="reports.pdf"'

    doc = SimpleDocTemplate(response)

    styles = getSampleStyleSheet()

    elements = []

    reports = Report.objects.all()

    for report in reports:

        elements.append(
            Paragraph(f"<b>Type:</b> {report.report_type}", styles['Normal'])
        )

        elements.append(
            Paragraph(f"<b>Location:</b> {report.location}", styles['Normal'])
        )

        elements.append(
            Paragraph(f"<b>Status:</b> {report.status}", styles['Normal'])
        )

        elements.append(
            Paragraph(f"<b>Priority:</b> {report.priority}", styles['Normal'])
        )

        elements.append(
            Spacer(1, 12)
        )

    doc.build(elements)

    return response