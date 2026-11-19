package mx.itson.estudiantes.api;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.google.gson.reflect.TypeToken;
import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.List;
import mx.itson.estudiantes.entities.Estudiante;

public class ApiClient {

    private static final String URL = "http://127.0.0.1:8000/estudiante";

    private final HttpClient client = HttpClient.newHttpClient();
    private final Gson gson = new Gson();

    // GET /estudiante
    public List<Estudiante> listar() throws Exception {
        HttpRequest request = HttpRequest
                .newBuilder()
                .uri(URI.create(URL))
                .GET()
                .build();
        HttpResponse<String> response = enviar(request);
        return gson.fromJson(response.body(), new TypeToken<List<Estudiante>>() {}.getType());
    }

    // POST /estudiante si es nuevo (id = 0), PUT /estudiante/id si ya existe
    public void guardar(Estudiante estudiante) throws Exception {
        String json = gson.toJson(estudiante);
        HttpRequest.Builder builder = HttpRequest.newBuilder()
                .header("Content-Type", "application/json");
        if (estudiante.getId() == 0) {
            builder.uri(URI.create(URL)).POST(HttpRequest.BodyPublishers.ofString(json));
        } else {
            builder.uri(URI.create(URL + "/" + estudiante.getId()))
                    .PUT(HttpRequest.BodyPublishers.ofString(json));
        }
        enviar(builder.build());
    }

    // DELETE /estudiante/id
    public void eliminar(int id) throws Exception {
        HttpRequest request = HttpRequest
                .newBuilder()
                .uri(URI.create(URL + "/" + id))
                .DELETE()
                .build();
        enviar(request);
    }

    // Manda la petición. Si la API responde con error, lo lanza con su mensaje
    private HttpResponse<String> enviar(HttpRequest request) throws Exception {
        try {
            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
            if (response.statusCode() >= 400) {
                JsonObject json = gson.fromJson(response.body(), JsonObject.class);
                throw new Exception(json.get("error").getAsString());
            }
            return response;
        } catch (IOException ex) {
            throw new Exception("No se pudo conectar con la API");
        }
    }
}
