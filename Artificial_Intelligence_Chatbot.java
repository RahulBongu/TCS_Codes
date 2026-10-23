import javax.swing.*;
import java.awt.*;
import java.io.*;
import java.util.HashMap;
import java.util.Map;

public class  Artificial_Intelligence_Chatbot  extends JFrame {

    private JTextArea chatArea;
    private JTextField inputField;
    private JButton sendButton;

    private Map<String, String> knowledgeBase = new HashMap<>();

    private boolean waitingForTeaching = false;
    private String lastUnknownQuestion = "";

    // ================= COLORS =================
    private final Color BG_BLACK = new Color(10, 10, 10);
    private final Color PANEL_BLACK = new Color(18, 18, 18);
    private final Color GREEN = new Color(0, 255, 120);
    private final Color TEXT_WHITE = new Color(220, 220, 220);

    public  Artificial_Intelligence_Chatbot () {
        setTitle("NeuroChat AI // Cyber Edition");
        setSize(700, 600);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);

        initializeKnowledgeBase();
        buildGUI();

        addMessage("NEUROBOT",
                "SYSTEM ONLINE...\nHello Human.\nI am NeuroChat AI.");

        setVisible(true);
    }

    // ================= UI =================
    private void buildGUI() {

        setLayout(new BorderLayout());

        // TITLE
        JLabel title = new JLabel("NEUROCHAT AI TERMINAL", SwingConstants.CENTER);
        title.setOpaque(true);
        title.setBackground(BG_BLACK);
        title.setForeground(GREEN);
        title.setFont(new Font("Monospaced", Font.BOLD, 22));
        title.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        // CHAT AREA
        chatArea = new JTextArea();
        chatArea.setEditable(false);
        chatArea.setFont(new Font("Monospaced", Font.PLAIN, 14));
        chatArea.setBackground(BG_BLACK);
        chatArea.setForeground(GREEN);
        chatArea.setCaretColor(GREEN);
        chatArea.setLineWrap(true);
        chatArea.setWrapStyleWord(true);

        JScrollPane scrollPane = new JScrollPane(chatArea);
        scrollPane.setBorder(BorderFactory.createLineBorder(GREEN));

        // INPUT FIELD
        inputField = new JTextField();
        inputField.setBackground(BG_BLACK);
        inputField.setForeground(TEXT_WHITE);
        inputField.setCaretColor(GREEN);
        inputField.setFont(new Font("Monospaced", Font.PLAIN, 14));
        inputField.setBorder(BorderFactory.createLineBorder(GREEN));

        // ================= SEND BUTTON (BALANCED SIZE) =================
        sendButton = new JButton("SEND");
        sendButton.setPreferredSize(new Dimension(110, 38)); // 👈 balanced size
        sendButton.setBackground(BG_BLACK);
        sendButton.setForeground(GREEN);
        sendButton.setFont(new Font("Monospaced", Font.BOLD, 14));
        sendButton.setFocusPainted(false);
        sendButton.setBorder(BorderFactory.createLineBorder(GREEN, 2));
        sendButton.setCursor(new Cursor(Cursor.HAND_CURSOR));

        // BUTTON WRAPPER (prevents squeezing)
        JPanel buttonWrapper = new JPanel();
        buttonWrapper.setBackground(PANEL_BLACK);
        buttonWrapper.add(sendButton);

        // BOTTOM PANEL
        JPanel bottomPanel = new JPanel(new BorderLayout(8, 0));
        bottomPanel.setBackground(PANEL_BLACK);
        bottomPanel.add(inputField, BorderLayout.CENTER);
        bottomPanel.add(buttonWrapper, BorderLayout.EAST);

        add(title, BorderLayout.NORTH);
        add(scrollPane, BorderLayout.CENTER);
        add(bottomPanel, BorderLayout.SOUTH);

        sendButton.addActionListener(e -> processInput());
        inputField.addActionListener(e -> processInput());
    }

    // ================= CHAT LOGIC =================
    private void processInput() {

        String userInput = inputField.getText().trim();
        if (userInput.isEmpty()) return;

        addMessage("YOU", userInput);

        if (waitingForTeaching) {
            teachBot(userInput);
            inputField.setText("");
            return;
        }

        String response = generateResponse(userInput);
        addMessage("NEUROBOT", response);

        inputField.setText("");
    }

    // ================= RESPONSE ENGINE =================
    private String generateResponse(String input) {

        String cleaned = preprocess(input);
        String sentiment = detectSentiment(cleaned);

        if (!sentiment.equals("neutral")) {
            return "Sentiment detected: " + sentiment.toUpperCase();
        }

        for (String key : knowledgeBase.keySet()) {
            if (cleaned.contains(key)) {
                return knowledgeBase.get(key);
            }
        }

        if (cleaned.contains("time")) {
            return "TIME MODULE OFFLINE";
        }

        if (cleaned.contains("name")) {
            return "I am NeuroChat AI v1.0";
        }

        lastUnknownQuestion = cleaned;
        waitingForTeaching = true;

        return "UNKNOWN INPUT DETECTED.\nTeach me the response:";
    }

    // ================= LEARNING =================
    private void teachBot(String answer) {

        knowledgeBase.put(lastUnknownQuestion, answer);
        saveKnowledgeBase();

        addMessage("SYSTEM", "LEARNING COMPLETE. DATA STORED.");

        waitingForTeaching = false;
        lastUnknownQuestion = "";
    }

    // ================= NLP =================
    private String preprocess(String text) {
        return text.toLowerCase()
                .replaceAll("[^a-z0-9 ]", "")
                .trim();
    }

    private String detectSentiment(String text) {

        String[] positive = {"good", "great", "awesome", "happy", "love"};
        String[] negative = {"bad", "sad", "angry", "hate", "terrible"};

        for (String p : positive)
            if (text.contains(p)) return "positive";

        for (String n : negative)
            if (text.contains(n)) return "negative";

        return "neutral";
    }

    // ================= KNOWLEDGE BASE =================
    private void initializeKnowledgeBase() {

        File file = new File("knowledge.txt");

        if (file.exists()) {
            loadKnowledgeBase();
            return;
        }

        knowledgeBase.put("hello", "HELLO HUMAN");
        knowledgeBase.put("hi", "GREETINGS USER");
        knowledgeBase.put("what is java", "JAVA IS A PROGRAMMING LANGUAGE");
        knowledgeBase.put("what is ai", "AI = ARTIFICIAL INTELLIGENCE");
        knowledgeBase.put("bye", "SYSTEM SHUTTING DOWN...");
    }

    private void saveKnowledgeBase() {

        try (PrintWriter pw = new PrintWriter(new FileWriter("knowledge.txt"))) {
            for (Map.Entry<String, String> e : knowledgeBase.entrySet()) {
                pw.println(e.getKey() + "|" + e.getValue());
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void loadKnowledgeBase() {

        try (BufferedReader br = new BufferedReader(new FileReader("knowledge.txt"))) {

            String line;
            while ((line = br.readLine()) != null) {
                String[] parts = line.split("\\|", 2);
                if (parts.length == 2) {
                    knowledgeBase.put(parts[0], parts[1]);
                }
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // ================= UI HELPER =================
    private void addMessage(String sender, String msg) {
        chatArea.append("[" + sender + "]\n" + msg + "\n\n");
        chatArea.setCaretPosition(chatArea.getDocument().getLength());
    }

    // ================= MAIN =================
    public static void main(String[] args) {
        SwingUtilities.invokeLater( Artificial_Intelligence_Chatbot ::new);
    }
}