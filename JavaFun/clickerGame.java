package JavaFun;

import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class clickerGame {
    private static int score = 0;

    public static void main(String[] args) {
        JFrame frame = new JFrame("Simple Clicker Game");
        JButton increaseButton = new JButton("Increase");
        JButton decreaseButton = new JButton("Decrease");
        JButton exitButton = new JButton("Exit");
        JLabel label = new JLabel("Score: 0");

        increaseButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                score++;
                label.setText("Score: " + score);
            }
        });

        decreaseButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                score--;
                label.setText("Score: " + score);
            }
        });

        exitButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                System.exit(0);
            }
        });

        frame.setLayout(new java.awt.FlowLayout());
        frame.add(increaseButton);
        frame.add(decreaseButton);
        frame.add(exitButton);
        frame.add(label);
        frame.setSize(300, 100);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setVisible(true);
    }
}
