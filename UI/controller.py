import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDs(self):
        years = self._model.getYears()
        for y in years:
            self._view._ddYear1.options.append(ft.dropdown.Option(y))
            self._view._ddYear2.options.append(ft.dropdown.Option(y))
        self._view.update_page()


    def handleBuildGraph(self, e):
        self._view._txtGraphDetails.controls.clear()
        year1 = self._view._ddYear1.value
        if not year1:
            self._view._txtGraphDetails.controls.append(ft.Text("Selezionare l'anno iniziale", color="red"))
            self._view.update_page()
            return
        year2 = self._view._ddYear2.value
        if not year2:
            self._view._txtGraphDetails.controls.append(ft.Text("Selezionare l'anno finale", color="red"))
            self._view.update_page()
            return
        if not year2 > year1:
            self._view._txtGraphDetails.controls.append(ft.Text("L'anno finale deve essere maggiore dell'anno inziale", color="red"))
            self._view.update_page()
            return
        nodes, edges = self._model.buildGraph(year1, year2)
        self._view._txtGraphDetails.controls.append(ft.Text("Grafo creato correttamente"))
        self._view._txtGraphDetails.controls.append(ft.Text(f"Il grafo contiene {nodes} nodi e {edges} archi"))
        self._view._btnPrintDetails.disabled = False
        self._view._btnCalcolaSoluzione.disabled = False
        self._view.update_page()


    def handlePrintDetails(self, e):
        self._view._txtGraphDetails.controls.clear()
        componenteConnessa = self._model.getComponenteConnessa()
        for c in componenteConnessa:
            self._view._txtGraphDetails.controls.append(ft.Text(f"{c} -- {self._model.getPesoMinimo(c)}"))
        self._view.update_page()


    def handleCercaDreamChampionship(self, e):
        pass

