package com.samueldillow.server;

import java.io.IOException;
import java.util.Scanner;

import javax.servlet.Filter;
import javax.servlet.FilterChain;
import javax.servlet.FilterConfig;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.http.HttpServletRequest;

import com.google.gwt.user.server.rpc.RemoteServiceServlet;

/**
 * The server side implementation of the RPC service.
 */
public class MainServlet extends RemoteServiceServlet implements Filter {
	/**
	 * Because the class is serializable 
	 */
	private static final long serialVersionUID = 1L;

	@Override
	public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {
		// Try to make the request into an HTTP request
		HttpServletRequest httpRequest = (HttpServletRequest) request;
		
		// If the conversion was successful
		if(httpRequest != null) {
			Scanner scanner = new Scanner(httpRequest.getRequestURI()).useDelimiter("/");
			
			if(scanner.hasNext()) {
				System.out.println("next: " + scanner.next());
			}
		}
		
		else System.out.println("Rqeuest not supported");
	}
	
	@Override
	public void init(FilterConfig config) throws ServletException { 
	}
}
