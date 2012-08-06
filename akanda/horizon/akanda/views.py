from horizon import tabs

from tabs import NetworkingTabs


class IndexView(tabs.TabbedTableView):
    template_name = 'akanda/index.html'
    tab_group_class = NetworkingTabs

    def get(self, request, *args, **kwargs):
        return super(IndexView, self).get(request, *args, **kwargs)