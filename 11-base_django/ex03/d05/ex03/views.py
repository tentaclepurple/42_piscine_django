from django.shortcuts import render


def shades_table(request):

    step = 5.1 # 255 / 50
    context = {
        "range": [int(i * step) for i in range(50)]
    }
    return render(request, 'shades_table.html', context)
