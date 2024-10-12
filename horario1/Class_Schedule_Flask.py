from flask import Flask, render_template, redirect, url_for, flash, request
app = Flask (__name__)
app.secret_key='supersecretkey'
from tabulate import tabulate

class Clase:
    def __init__(self, profe, nombre, dia, hora, grupo):
        self.profe = profe
        self.nombre = nombre
        self.dia = dia
        self.hora = hora
        self.grupo = grupo

class Horario:
    def __init__(self):
        self.clases = []

    def agregar_clase(self, profe, nombre, dia, hora, grupo):
        nueva_clase = Clase(profe, nombre, dia, hora, grupo)
        self.clases.append(nueva_clase)
        print(f'la clase{nombre} esta dentro')

    def eliminar_clase(self, dia, hora):
        if not self.clases:
            print('el horario esta vacio, mete una clase')
            return

        nombre_clase = input('qye clase quieres borrar?')
        dia = input('se que día?')
        hora = input('a que hora?')

        for clase in self.clases:
            if clase[nombre_clase] == nombre_clase and clase[dia] == dia and clase[hora] == hora:
                self.clases.remove(clase)
            print(f'la clase ya no esta')
            return
        
    print('no se encontró la clase, verifique su marcación')


    def mostrar_horario(self):
        if not self.clases:
            print('el horario está vacio')
            return
        dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
        clases_ordenadas = sorted(self.clases, key=lambda x: (x[profe], x[nombre_clase], dias_semana.index(x[dia]), x[hora]))
        
        tabla = []
        for clase in clases_ordenadas:
            tabla.append([clase.dia, clase.hora, clase.nombre, clase.profe, clase.grupo])
        

        encabezados = ['profe', 'clase', 'dia', 'hora', 'grupo']
        
        print(tabulate(tabla, headers=encabezados, tablefmt='html'))
        
        total_clases = len(self.clases)
        print(f'al final tienes {total_clases} horas de clases a la semana')


horario = Horario()
    
@app.route('/')
def index():
    return render_template('inicio.html')
@app.route("/agregar_clase", methods=['GET','POST'])
def agregar_clase():
    if request.method == 'POST':
        profe = request.form['profe']
        nombre = request.form['nombre']
        dia = request.form['dia']
        hora = request.form['hora']
        grupo = request.form['grupo']
        horario.agregar_clase(profe, nombre, dia, hora, grupo)
        return redirect(url_for('index'))
    return render_template('agregar_clase.html')

@app.route("/eliminar_clase", methods=['GET', 'POST'])
def eliminar_clase():
    if request.method == 'POST':
        dia = request.form['día']
        hora = request.form['hora']
        nombre_clase = request.form['nombre_clase']
        horario.eliminar_clase(dia, hora, nombre_clase)
        return redirect(url_for('index'))
    return render_template('eliminar_horario.html')

@app.route('/mostrar_horario', methods=['GET', 'POST'])
def mostrar_horario():
    if request.method == 'POST':
        dia = request.form['dia']
        hora = request.form['hora']
        if horario.clases:
            horario.mostrar_horario(dia, hora)
            return render_template('mostrar_horario.html', clases=horario.clases)
        else:
            flash('No hay clases en el horario')
        return redirect(url_for('agregar_clase'))
    return render_template('mostrar_horario.html')

if __name__ == '__main__':
    app.run(debug=True)