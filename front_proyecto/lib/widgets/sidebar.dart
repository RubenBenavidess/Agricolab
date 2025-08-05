// widgets/sidebar.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../viewmodels/chat_viewmodel.dart';

// widgets/sidebar.dart - Hacer el sidebar responsivo

class Sidebar extends StatelessWidget {
  const Sidebar({super.key});

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;
    final isMobile = screenWidth < 600;
    final isTablet = screenWidth >= 600 && screenWidth < 900;

    return Consumer<ChatViewModel>(
      builder: (context, viewModel, child) {
        return Column(
          children: [
            // Header - Adaptativo
            Container(
              padding: EdgeInsets.all(isMobile ? 12 : 16),
              child: Row(
                children: [
                  IconButton(
                    icon: Icon(
                      Icons.menu,
                      color: Colors.white70,
                      size: isMobile ? 20 : 24,
                    ),
                    onPressed: () => viewModel.toggleSidebar(),
                    tooltip: 'Ocultar menú',
                  ),
                  const Spacer(),
                  IconButton(
                    icon: Icon(
                      Icons.settings,
                      color: Colors.white70,
                      size: isMobile ? 20 : 24,
                    ),
                    onPressed: () {},
                  ),
                ],
              ),
            ),
            // New Chat Button - Adaptativo
            Padding(
              padding: EdgeInsets.symmetric(
                horizontal: isMobile ? 12 : 16,
                vertical: 8,
              ),
              child: SizedBox(
                width: double.infinity,
                child: ElevatedButton.icon(
                  onPressed: viewModel.createNewChat,
                  icon: Icon(
                    Icons.add,
                    color: Colors.white,
                    size: isMobile ? 16 : 20,
                  ),
                  label: Text(
                    'Nuevo chat',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: isMobile ? 12 : 14,
                    ),
                  ),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF404040),
                    padding: EdgeInsets.symmetric(vertical: isMobile ? 8 : 12),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(8),
                    ),
                  ),
                ),
              ),
            ),
            // Chats Section
            Padding(
              padding: EdgeInsets.symmetric(
                horizontal: isMobile ? 12 : 16,
                vertical: 8,
              ),
              child: Row(
                children: [
                  Icon(
                    Icons.chat_bubble_outline,
                    color: Colors.white70,
                    size: isMobile ? 16 : 20,
                  ),
                  const SizedBox(width: 8),
                  Text(
                    'Chats',
                    style: TextStyle(
                      color: Colors.white70,
                      fontSize: isMobile ? 14 : 16,
                    ),
                  ),
                ],
              ),
            ),
            // Chat List
            Expanded(
              child: ListView.builder(
                padding: EdgeInsets.symmetric(horizontal: isMobile ? 4 : 8),
                itemCount: viewModel.chats.length,
                itemBuilder: (context, index) {
                  final chat = viewModel.chats[index];
                  final isSelected = viewModel.currentChat?.id == chat.id;

                  return Container(
                    margin: const EdgeInsets.symmetric(vertical: 2),
                    decoration: BoxDecoration(
                      color: isSelected
                          ? const Color(0xFF404040)
                          : Colors.transparent,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: ListTile(
                      dense: isMobile, // Más compacto en móvil
                      contentPadding: EdgeInsets.symmetric(
                        horizontal: isMobile ? 8 : 12,
                        vertical: isMobile ? 2 : 4,
                      ),
                      title: Text(
                        chat.title,
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: isMobile ? 12 : 14,
                        ),
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                      onTap: () {
                        viewModel.selectChat(chat.id);
                        // Cerrar sidebar en móvil después de seleccionar
                      },
                      trailing: !isTablet
                          ? PopupMenuButton<String>(
                              icon: Icon(
                                Icons.more_vert,
                                color: Colors.white70,
                                size: isMobile ? 14 : 16,
                              ),
                              color: const Color(0xFF404040),
                              onSelected: (value) {
                                switch (value) {
                                  case 'rename':
                                    _showRenameDialog(
                                      context,
                                      viewModel,
                                      chat.id,
                                      chat.title,
                                    );
                                    break;
                                  case 'delete':
                                    viewModel.deleteChat(chat.id);
                                    break;
                                }
                              },
                              itemBuilder: (context) => [
                                const PopupMenuItem(
                                  value: 'rename',
                                  child: Row(
                                    children: [
                                      Icon(
                                        Icons.edit,
                                        color: Colors.white70,
                                        size: 16,
                                      ),
                                      SizedBox(width: 8),
                                      Text(
                                        'Renombrar',
                                        style: TextStyle(color: Colors.white),
                                      ),
                                    ],
                                  ),
                                ),
                                const PopupMenuItem(
                                  value: 'delete',
                                  child: Row(
                                    children: [
                                      Icon(
                                        Icons.delete,
                                        color: Colors.red,
                                        size: 16,
                                      ),
                                      SizedBox(width: 8),
                                      Text(
                                        'Eliminar',
                                        style: TextStyle(color: Colors.red),
                                      ),
                                    ],
                                  ),
                                ),
                              ],
                            )
                          : null,
                    ),
                  );
                },
              ),
            ),
          ],
        );
      },
    );
  }

  void _showRenameDialog(
    BuildContext context,
    ChatViewModel viewModel,
    String chatId,
    String currentTitle,
  ) {
    final controller = TextEditingController(text: currentTitle);
    final screenWidth = MediaQuery.of(context).size.width;
    final isMobile = screenWidth < 600;

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        backgroundColor: const Color(0xFF2A2A2A),
        title: Text(
          'Renombrar Chat',
          style: TextStyle(color: Colors.white, fontSize: isMobile ? 16 : 18),
        ),
        content: TextField(
          controller: controller,
          style: TextStyle(color: Colors.white, fontSize: isMobile ? 14 : 16),
          decoration: const InputDecoration(
            hintText: 'Nuevo nombre',
            hintStyle: TextStyle(color: Colors.white54),
            enabledBorder: UnderlineInputBorder(
              borderSide: BorderSide(color: Colors.white54),
            ),
            focusedBorder: UnderlineInputBorder(
              borderSide: BorderSide(color: Colors.blue),
            ),
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancelar'),
          ),
          TextButton(
            onPressed: () {
              if (controller.text.trim().isNotEmpty) {
                viewModel.renameChat(chatId, controller.text.trim());
                Navigator.pop(context);
              }
            },
            child: const Text('Guardar'),
          ),
        ],
      ),
    );
  }
}
