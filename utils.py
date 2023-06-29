import numpy as np
from OpenGL.GL import *
import ctypes


def getObj(path):
    numberOfFacesWith3Vertices = 0
    numberOfFacesWith4Vertices = 0
    numberOfFacesWithMoreThan4Vertices = 0
    tex_coords = []
    dropped = 1
    fileName = path.split('\\')[-1]
    if (path.split('.')[1].lower() != "obj"):
        print("Invalid File\nPlease provide an .obj file")
        return
    with open(path) as f:
        lines = f.readlines()
        vStrings = [x.strip('v') for x in lines if x.startswith('v ')]
        vertices = convertVertices(vStrings)
        if np.amax(vertices) <= 1.2:
            vertices /= np.amax(vertices)
        else:
            vertices /= np.amax(vertices) / 2
        vnStrings = [x.strip('vn') for x in lines if x.startswith('vn')]
        if not vnStrings:  # if There is no normal vectors in the obj file then compute them
            normals = fillNormalsArray(len(vStrings), vertices)
        else:
            normals = convertVertices(vnStrings)
        faces = [x.strip('f') for x in lines if x.startswith('f')]

        vtStrings = [x.strip('vt') for x in lines if x.startswith('vt')]
        for vtString in vtStrings:
            for i in vtString.split('\n')[0].split(' ')[1:]:
                tex_coords.append(float(i))

    for face in faces:
        if len(face.split()) == 3:
            numberOfFacesWith3Vertices += 1
        elif len(face.split()) == 4:
            numberOfFacesWith4Vertices += 1
        else:
            numberOfFacesWithMoreThan4Vertices += 1
    if numberOfFacesWith4Vertices > 0 or numberOfFacesWithMoreThan4Vertices > 0:
        faces = triangulate(faces)
    gVertexArraySeparate = createVertexArraySeparate(faces, normals, vertices)

    return gVertexArraySeparate, tex_coords

def extractMtl(mtl_filename):
    # Aqui você pode abrir e ler o arquivo .mtl, semelhante ao que foi feito com o .obj
    with open(mtl_filename) as f:
        mtl_lines = f.readlines()

    # Aqui você pode percorrer as linhas do arquivo .mtl e extrair as informações desejadas
    # por exemplo, você pode procurar pelas linhas que começam com 'Kd' para extrair a cor difusa

    for line in mtl_lines:
        if line.startswith('Kd'):
            # Extrair a cor difusa (exemplo de implementação)
            color_components = line.split()[1:]  # Obter os componentes da cor
            color = [float(c) for c in color_components]  # Converter os componentes em floats
            print("Diffuse Color:", color)  # Exemplo: imprimir a cor difusa

    # Você pode adicionar o código para extrair outras informações do arquivo .mtl, como cores especulares, texturas, etc.



def draw_glDrawArray(gVertexArraySeparate, tex_coords):
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glEnableClientState(GL_TEXTURE_COORD_ARRAY)

    # Define o ponteiro para o array de vértices
    glVertexPointer(3, GL_FLOAT, 6 * gVertexArraySeparate.itemsize, ctypes.c_void_p(gVertexArraySeparate.ctypes.data + 3 * gVertexArraySeparate.itemsize))

    # Define o ponteiro para o array de normais
    glNormalPointer(GL_FLOAT, 6 * gVertexArraySeparate.itemsize, gVertexArraySeparate)

    glTexCoordPointer(2, GL_FLOAT, 0, tex_coords)

    # Desenha os triângulos usando os arrays de vértices e normais
    glDrawArrays(GL_TRIANGLES, 0, int(gVertexArraySeparate.size / 6))

    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_NORMAL_ARRAY)
    glDisableClientState(GL_TEXTURE_COORD_ARRAY)

    glFlush()


    # # Define o ponteiro para o array de normais
    # glNormalPointer(GL_FLOAT, 6 * gVertexArraySeparate.itemsize, gVertexArraySeparate)
    #
    # # Define o ponteiro para o array de vértices
    # glVertexPointer(3, GL_FLOAT, 6 * gVertexArraySeparate.itemsize, ctypes.c_void_p(gVertexArraySeparate.ctypes.data + 3 * gVertexArraySeparate.itemsize))
    #
    # glTexCoordPointer(2, GL_FLOAT, 0, tex_coords)
    #
    # # Desenha os triângulos usando os arrays de vértices e normais
    # glDrawArrays(GL_TRIANGLES, 0, int(gVertexArraySeparate.size / 6))

def triangulate(faces):
    facesList = []  # Lista para armazenar as faces trianguladas
    nPolygons = []  # Lista para armazenar as faces que não são polígonos de três vértices
    for face in faces:
        if len(face.split()) >= 4:
            # Se a face tiver mais de três vértices, é adicionada à lista de polígonos
            nPolygons.append(face)
        else:
            # Caso contrário, é adicionada diretamente à lista de faces trianguladas
            facesList.append(face)

    for face in nPolygons:
        # Para cada polígono com mais de três vértices
        for i in range(1, len(face.split()) - 1):
            # Triangula o polígono dividindo-o em triângulos consecutivos
            seq = [str(face.split()[0]), str(face.split()[i]), str(face.split()[i + 1])]
            string = ' '.join(seq)
            # Junta os vértices do triângulo em uma string separada por espaços
            facesList.append(string)

    return facesList  # Retorna a lista de faces trianguladas


def createVertexArraySeparate(faces, normals, vertices):
    varr = np.zeros((len(faces) * 6, 3), 'float32')  # Array para armazenar os vértices e normais separadamente
    i = 0  # Índice para percorrer o array varr
    normalsIndex = 0  # Índice para acessar as normais
    verticeIndex = 0  # Índice para acessar os vértices
    for face in faces:
        for f in face.split():
            if '//' in f:  # Verifica se a face tem normais definidas
                verticeIndex = int(f.split('//')[0]) - 1  # Obtém o índice do vértice
                normalsIndex = int(f.split('//')[1]) - 1  # Obtém o índice da normal
            elif '/' in f:  # Verifica se a face tem texturas ou normais definidas
                if len(f.split('/')) == 2:  # Verifica se tem texturas definidas
                    verticeIndex = int(f.split('/')[0]) - 1  # Obtém o índice do vértice
                    normalsIndex = int(f.split('/')[0]) - 1  # Obtém o índice da normal
                else:  # Tem texturas e normais definidas
                    verticeIndex = int(f.split('/')[0]) - 1  # Obtém o índice do vértice
                    normalsIndex = int(f.split('/')[2]) - 1  # Obtém o índice da normal
            else:  # Se não tem normais nem texturas definidas
                verticeIndex = int(f.split()[0]) - 1  # Obtém o índice do vértice
                normalsIndex = int(f.split()[0]) - 1  # Obtém o índice da normal
            varr[i] = normals[normalsIndex]  # Armazena a normal no array varr
            varr[i + 1] = vertices[verticeIndex]  # Armazena o vértice no array varr
            i += 2  # Incrementa o índice do array varr
    return varr  # Retorna o array varr com os vértices e normais separados


def convertVertices(verticesStrings):
    # Cria uma matriz de zeros com o tamanho igual ao número de strings de vértices e três colunas
    v = np.zeros((len(verticesStrings), 3))
    i = 0
    # Itera sobre as strings de vértices
    for vertice in verticesStrings:
        j = 0
        # Divide a string do vértice em partes separadas e itera sobre elas
        for t in vertice.split():
            try:
                # Converte cada parte em um número de ponto flutuante e atribui à matriz de vértices
                v[i][j] = (float(t))
            except ValueError:
                # Ignora partes que não podem ser convertidas em float
                pass
            j += 1
        i += 1
    # Retorna a matriz de vértices convertida
    return v


def fillNormalsArray(numberOfVertices, vertices):
    # Cria um array de zeros com o tamanho do número de vértices e três colunas
    normals = np.zeros((numberOfVertices, 3))
    i = 0
    # Itera sobre os vértices
    for vertice in vertices:
        # Normaliza o vértice usando uma função chamada normalized
        normals[i] = normalized(vertice)
        i += 1
    # Retorna o array de normais preenchido
    return normals


def l2norm(v):
    return np.sqrt(np.dot(v, v))


def normalized(v):
    l = l2norm(v)
    return 1 / l * np.array(v)


def framebuffer_size_callback(window, width, height):
    glViewport(0, 0, width, height)
