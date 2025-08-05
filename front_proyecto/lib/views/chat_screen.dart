// views/chat_screen.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../viewmodels/chat_viewmodel.dart';
import '../widgets/sidebar.dart';
import '../widgets/chat_area.dart';

class ChatScreen extends StatelessWidget {
  const ChatScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (_) => ChatViewModel(),
      child: const ChatView(),
    );
  }
}

// views/chat_screen.dart - Actualizar la clase ChatView

class ChatView extends StatelessWidget {
  const ChatView({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF1E1E1E),
      body: Consumer<ChatViewModel>(
        builder: (context, viewModel, child) {
          final screenWidth = MediaQuery.of(context).size.width;
          final sidebarWidth = viewModel.getSidebarWidth(screenWidth);
          final isMobile = screenWidth < 600;

          // Actualizar el estado basado en el tamaño de pantalla
          WidgetsBinding.instance.addPostFrameCallback((_) {
            viewModel.updateScreenSize(screenWidth);
          });
          return Stack(
            children: [
              // Layout principal
              Row(
                children: [
                  // Espacio reservado para sidebar (solo en no-móvil)
                  if (!isMobile)
                    AnimatedContainer(
                      duration: const Duration(milliseconds: 300),
                      curve: Curves.easeInOut,
                      width: viewModel.isSidebarVisible ? sidebarWidth : 0,
                    ),
                  // Chat Area
                  const Expanded(child: ChatArea()),
                ],
              ),
              // Sidebar superpuesto
              if (viewModel.isSidebarVisible)
                AnimatedPositioned(
                  duration: const Duration(milliseconds: 300),
                  curve: Curves.easeInOut,
                  left: 0,
                  top: 0,
                  bottom: 0,
                  width: sidebarWidth,
                  child: Container(
                    decoration: BoxDecoration(
                      color: const Color(0xFF2A2A2A),
                      border: const Border(
                        right: BorderSide(color: Color(0xFF404040), width: 1),
                      ),
                      // Sombra en móvil para efecto overlay
                      boxShadow: isMobile
                          ? [
                              BoxShadow(
                                color: Colors.black.withOpacity(0.5),
                                blurRadius: 10,
                                offset: const Offset(2, 0),
                              ),
                            ]
                          : null,
                    ),
                    child: const Sidebar(),
                  ),
                ),
              // Overlay oscuro en móvil cuando el sidebar está visible
              if (isMobile && viewModel.isSidebarVisible)
                AnimatedOpacity(
                  duration: const Duration(milliseconds: 200),
                  opacity: 0.5,
                  child: GestureDetector(
                    onTap: () => viewModel.toggleSidebar(),
                    child: Container(
                      color: Colors.black,
                      width: double.infinity,
                      height: double.infinity,
                      margin: EdgeInsets.only(left: sidebarWidth),
                    ),
                  ),
                ),
            ],
          );
        },
      ),
    );
  }
}
