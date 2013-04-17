package com.samueldillow.server;

import java.io.File;
import java.io.IOException;
import java.util.Scanner;

import javax.servlet.Filter;
import javax.servlet.FilterChain;
import javax.servlet.FilterConfig;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

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
			// Get the uri of the request
			String uri = httpRequest.getRequestURI();
			// Make a scanner to parse the url
			Scanner scanner = new Scanner(uri).useDelimiter("/");
			// Figure out what the action of this url is
			String action = scanner.hasNext() ? scanner.next() : "";
			
			switch(action.hashCode()) {
				// Send the request to this class' request handler
				case 0                         : request.getRequestDispatcher("MainServlet").include(request, response)     ; break;
				case /* edit */ 0x2F6E0A       : request.getRequestDispatcher("MainServlet").include(request, response)     ; break;
				case /* resources */ 0x89CCBE25: filterResourceRequest(httpRequest, response); break; 
				
				default:
					// See if we can get the extension of the request (default to "")
					String type = new Scanner(action).findInLine("(?<=\\.).*?$");
					
					// Couldn't resolve action, so try type
					switch(type != null ? type.hashCode() : 0) {
						case /* css */ 0x18203: filterResourceRequest(httpRequest, response); break;
						
						default:
							System.out.printf("Unable to route%s request (%s) for url: %s\n"
									, type == null ? "" : type
									, action
									, httpRequest.getRequestURI()
									);
					}
					break;
			}
		}
		
		// Request not supported: Invoke the next entity in the chain using the FilterChain object
		else chain.doFilter(request, response);
	}
	
	/**
	 * Filters a request, but using resource finding logic
	 * 
	 * @param request  The request from JEE
	 * @param response The response to which to write a response
	 */
	private void filterResourceRequest(HttpServletRequest request, ServletResponse response) {
		// Get the uri from the request
		String uri = "." + request.getRequestURI();
		// The type of the file we're supposed to be serving
		String type = new Scanner(uri).findInLine("(?<=\\.)[^\\.]*?$");
		// The file that matches the request
		File file;
		
		// First start with uri
		file = new File(uri);
		// Next look in resources/(type)...
		if(!file.exists()) file = new File(uri.replaceAll("resources/(.*?)", "resources/"+type+"/$1"));
		// Finally look in **/(type)/(file)
		if(!file.exists()) file = new File(uri.replaceAll("(.*)/(.*?)$1", "$1/"+type+"/$2"));
		
		
		try {
			// Stream the file
			request.getRequestDispatcher("/" + file.getPath()).include(request, response);
		} catch (Throwable e) {
			e.printStackTrace();
		}
	}

	@Override
	public void init(FilterConfig config) throws ServletException { 
	}
	
	@Override
	protected void service(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// Get the uri part of the request
		String uri = request.getRequestURI();
		// Make a scanner to process the uri
		Scanner scanner = new Scanner(uri).useDelimiter("/");
		// If there is a next item, then get it. Otherwise use an empty string
		String action = scanner.hasNext() ? scanner.next() : "";
		
		switch(action.hashCode()) {
			case 0:
			default:
				// Send request to SamuelDillow.html
				request.getRequestDispatcher("/pages/SamuelDillow.jsp").include(request, response);
				break;
		}
	}
}
