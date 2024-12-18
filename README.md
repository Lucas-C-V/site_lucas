<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Solar App</title>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <style>
        #loading {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255, 255, 255, 0.8);
            z-index: 1000;
            text-align: center;
            padding-top: 200px;
            font-size: 24px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h1>Simulador de Células Fotovoltaicas</h1>
    <form id="graph-form">
        <label for="icc">Corrente de Curto-Circuito (Icc):</label>
        <input type="text" id="icc" name="icc" required><br><br>

        <label for="kt">Coeficiente de Temperatura (Kt):</label>
        <input type="text" id="kt" name="kt" required><br><br>

        <label for="vdc">Tensão de Circuito Aberto (Vdc):</label>
        <input type="text" id="vdc" name="vdc" required><br><br>

        <label for="vmp">Tensão de Máxima Energia (Vmp):</label>
        <input type="text" id="vmp" name="vmp" required><br><br>

        <button type="submit">Gerar Gráficos</button>
    </form>

    <div id="loading">Gerando gráficos, aguarde...</div>

    <h2>Gráficos Gerados</h2>
    <div id="graphs">
        {% if graph_paths %}
            {% for path in graph_paths %}
                <img src="{{ path }}" alt="Graph" style="width: 100%; max-width: 600px; margin-top: 20px;">
            {% endfor %}
        {% endif %}
    </div>

    <script>
        $(document).ready(function () {
            $("#graph-form").on("submit", function (e) {
                e.preventDefault();
                $("#loading").show();
                $("#graphs").empty();
                $.post("/generate_graphs", $(this).serialize(), function (data) {
                    $("#loading").hide();
                    data.forEach(function (path) {
                        $("#graphs").append(`<img src="${path}" alt="Graph" style="width: 100%; max-width: 600px; margin-top: 20px;">`);
                    });
                });
            });
        });
    </script>
</body>
</html>
