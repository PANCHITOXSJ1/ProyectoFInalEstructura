from pathlib import Path
from app_vuelos import GrafoVuelos

g = GrafoVuelos.desde_archivo(Path(__file__).with_name('vuelos.txt'))
casos = [
    ('Quito', 'Loja', 111.00, ['Quito','Cuenca','Loja']),
    ('Tena', 'Guayaquil', 139.00, ['Tena','Quito','Guayaquil']),
    ('Manta', 'Quito', 129.00, ['Manta','Guayaquil','Quito']),
    ('Coca', 'Loja', 168.00, ['Coca','Quito','Cuenca','Loja']),
    ('Cuenca', 'Manta', 94.00, ['Cuenca','Guayaquil','Manta']),
]
print('PRUEBAS FUNCIONALES')
print('='*82)
for i,(o,d,esperado,ruta_esperada) in enumerate(casos,1):
    costo,ruta=g.ruta_mas_barata(o,d)
    ok=abs(costo-esperado)<1e-9 and ruta==ruta_esperada
    print(f'{i}. {o:10s}->{d:10s} | esperado ${esperado:6.2f} | obtenido ${costo:6.2f} | {"OK" if ok else "FALLO"}')
    assert ok
print('Resultado: 5/5 pruebas superadas.')
