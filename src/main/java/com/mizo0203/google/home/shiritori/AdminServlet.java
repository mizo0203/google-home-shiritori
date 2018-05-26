package com.mizo0203.google.home.shiritori;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

public class AdminServlet extends HttpServlet {

    @Override
    public void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        resp.getWriter().println("ここは管理者（Google アカウント）専用ページ");
    }

    @Override
    public void doPost(HttpServletRequest req, HttpServletResponse resp) throws IOException {
    }
}
