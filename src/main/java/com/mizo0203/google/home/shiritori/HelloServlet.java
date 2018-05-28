package com.mizo0203.google.home.shiritori;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.mizo0203.google.home.shiritori.data.Data;
import org.apache.commons.io.IOUtils;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.logging.Logger;

public class HelloServlet extends HttpServlet {

    private static final Logger LOG = Logger.getLogger(HelloServlet.class.getName());

    @Override
    public void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        // Web ページへ出力するサンプル
        resp.getWriter().println("hello, world");

        // JSON データを解析するサンプル
        Data data =
                new ObjectMapper()
                        .readValue(
                                "{\n"
                                        + "    \"name\": \"mizo0203\",\n"
                                        + "    \"email\": \"mizo0203@mizo0203.com\"\n"
                                        + "  }",
                                Data.class);
        LOG.info("doPost() data: " + data);
    }

    @Override
    public void doPost(HttpServletRequest req, HttpServletResponse resp) throws IOException {

        // サーバーが受けたデータ
        // OSS ライブラリ「Apache Commons IO」を導入すると
        // InputStream 型から String 型へ 1 発変換できる
        String body = IOUtils.toString(req.getInputStream(), StandardCharsets.UTF_8);
        LOG.info("doPost() body: " + body);
    }
}
