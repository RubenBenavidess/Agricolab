// widgets/chat_area.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../viewmodels/chat_viewmodel.dart';
import 'message_bubble.dart';
import 'typing_indicator.dart';
import 'package:flutter/services.dart';

class ChatArea extends StatefulWidget {
  const ChatArea({super.key});

  @override
  State<ChatArea> createState() => _ChatAreaState();
}

class _ChatAreaState extends State<ChatArea> {
  final TextEditingController _controller = TextEditingController();
  final ScrollController _scrollController = ScrollController();

  @override
  void dispose() {
    _controller.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Consumer<ChatViewModel>(
      builder: (context, viewModel, child) {
        if (viewModel.currentChat != null &&
            viewModel.currentChat!.messages.isNotEmpty) {
          _scrollToBottom();
        }

        return Column(
          children: [
            // Header
            Container(
              padding: const EdgeInsets.all(16),
              decoration: const BoxDecoration(
                border: Border(
                  bottom: BorderSide(color: Color(0xFF404040), width: 1),
                ),
              ),
              child: Row(
                children: [
                  // Mostrar botón del menú si el sidebar está oculto O si es móvil
                  Consumer<ChatViewModel>(
                    builder: (context, viewModel, child) {
                      final screenWidth = MediaQuery.of(context).size.width;
                      final isMobile = screenWidth < 600;
                      final shouldShowMenuButton =
                          !viewModel.isSidebarVisible || isMobile;

                      if (shouldShowMenuButton) {
                        return Row(
                          children: [
                            IconButton(
                              icon: Icon(
                                Icons.menu,
                                color: Colors.white70,
                                size: isMobile ? 20 : 24,
                              ),
                              onPressed: () => viewModel.toggleSidebar(),
                              tooltip: 'Mostrar menú',
                            ),
                            const SizedBox(width: 8),
                          ],
                        );
                      }
                      return const SizedBox.shrink();
                    },
                  ),
                  Expanded(
                    child: Consumer<ChatViewModel>(
                      builder: (context, viewModel, child) {
                        final screenWidth = MediaQuery.of(context).size.width;
                        final isMobile = screenWidth < 600;

                        return Text(
                          viewModel.currentChat?.title ?? 'AgricoLab Chat',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: isMobile ? 16 : 18,
                            fontWeight: FontWeight.w500,
                          ),
                          overflow: TextOverflow.ellipsis,
                        );
                      },
                    ),
                  ),
                  Consumer<ChatViewModel>(
                    builder: (context, viewModel, child) {
                      final screenWidth = MediaQuery.of(context).size.width;
                      final isMobile = screenWidth < 600;

                      return IconButton(
                        icon: Icon(
                          Icons.settings,
                          color: Colors.white70,
                          size: isMobile ? 20 : 24,
                        ),
                        onPressed: () {},
                      );
                    },
                  ),
                ],
              ),
            ),
            // Messages Area
            Expanded(
              child:
                  viewModel.currentChat == null ||
                      viewModel.currentChat!.messages.isEmpty
                  ? _buildWelcomeMessage()
                  : ListView.builder(
                      controller: _scrollController,
                      padding: const EdgeInsets.all(16),
                      itemCount: viewModel.currentChat!.messages.length,
                      itemBuilder: (context, index) {
                        final message = viewModel.currentChat!.messages[index];
                        return MessageBubble(message: message);
                      },
                    ),
            ),
            // Loading Indicator
            if (viewModel.isLoading)
              const Padding(
                padding: EdgeInsets.symmetric(horizontal: 16),
                child: TypingIndicator(),
              ),
            // Input Area
            Container(
              padding: const EdgeInsets.all(16),
              decoration: const BoxDecoration(
                border: Border(
                  top: BorderSide(color: Color(0xFF404040), width: 1),
                ),
              ),
              child: Row(
                children: [
                  Expanded(
                    child: Container(
                      decoration: BoxDecoration(
                        color: const Color(0xFF2A2A2A),
                        borderRadius: BorderRadius.circular(24),
                        border: Border.all(color: const Color(0xFF404040)),
                      ),
                      child: KeyboardListener(
                        focusNode: FocusNode(),
                        onKeyEvent: (KeyEvent event) {
                          // Detectar cuando se presiona Enter
                          if (event is KeyDownEvent &&
                              event.logicalKey == LogicalKeyboardKey.enter) {
                            // Si no se está presionando Shift, enviar mensaje
                            if (!HardwareKeyboard.instance.isShiftPressed) {
                              _sendMessage(viewModel);
                              return;
                            }
                            // Si se presiona Shift+Enter, permitir nueva línea (comportamiento por defecto)
                          }
                        },
                        child: TextField(
                          controller: _controller,
                          style: const TextStyle(color: Colors.white),
                          maxLines: null,
                          keyboardType: TextInputType.multiline,
                          textInputAction:
                              TextInputAction.newline, // Cambiar esto
                          decoration: const InputDecoration(
                            hintText:
                                'Para empezar, por favor, ingresa tu cultivo y ubicación en tu primera pregunta, o configúralos en el ícono de configuración.',
                            hintStyle: TextStyle(color: Colors.white54),
                            border: InputBorder.none,
                            contentPadding: EdgeInsets.symmetric(
                              horizontal: 20,
                              vertical: 12,
                            ),
                          ),
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Container(
                    decoration: BoxDecoration(
                      color: const Color(0xFF0084FF),
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: IconButton(
                      icon: const Icon(Icons.send, color: Colors.white),
                      onPressed: () => _sendMessage(viewModel),
                    ),
                  ),
                ],
              ),
            ),
          ],
        );
      },
    );
  }

  Widget _buildWelcomeMessage() {
    return const Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Text(
            'Bienvenido, Agricultor.',
            style: TextStyle(
              color: Color(0xFF4A9B8B),
              fontSize: 24,
              fontWeight: FontWeight.w500,
            ),
          ),
          SizedBox(height: 16),
          Text(
            '¿En qué puedo ayudarte hoy?',
            style: TextStyle(color: Colors.white70, fontSize: 16),
          ),
        ],
      ),
    );
  }

  void _sendMessage(ChatViewModel viewModel) {
    final message = _controller.text.trim();
    if (message.isNotEmpty && !viewModel.isLoading) {
      viewModel.sendMessage(message);
      _controller.clear();
    }
  }
}
