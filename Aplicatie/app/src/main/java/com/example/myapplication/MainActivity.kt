package com.example.myapplication

import MqttHelper
import android.annotation.SuppressLint
import android.app.Activity
import android.content.pm.ActivityInfo
import android.os.Bundle
import android.view.MotionEvent
import android.view.View
import android.webkit.WebView
import android.widget.Button
import android.widget.ImageButton
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    private lateinit var mqttHelper: MqttHelper

    @SuppressLint("ClickableViewAccessibility")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        this.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE)

        mqttHelper = MqttHelper()

        val brokerUrl = "tcp://192.168.98.228:1883"
        val clientId = "AndroidClient"
        mqttHelper.connect(brokerUrl, clientId)

        val webView = findViewById<WebView>(R.id.cameraView)
        val btnStartStream = findViewById<Button>(R.id.btnStartStream)
        val btnStopStream = findViewById<Button>(R.id.btnStopStream)
        btnStartStream.setOnClickListener{
            webView.visibility = View.VISIBLE
            webView.loadUrl("http://192.168.1.191")
            btnStartStream.visibility=View.GONE
            btnStopStream.visibility=View.VISIBLE
        }
        btnStopStream.setOnClickListener{
            webView.visibility = View.GONE
            btnStartStream.visibility=View.VISIBLE
            btnStopStream.visibility=View.GONE
        }

        val btnForward = findViewById<ImageButton>(R.id.btnForward)
        val btnBackward = findViewById<ImageButton>(R.id.btnBackward)
        val btnLeft = findViewById<ImageButton>(R.id.btnLeft)
        val btnRight = findViewById<ImageButton>(R.id.btnRight)
        val btnCamUp = findViewById<ImageButton>(R.id.btnCamUp)
        val btnCamDown = findViewById<ImageButton>(R.id.btnCamDown)
        val btnCamLeft = findViewById<ImageButton>(R.id.btnCamLeft)
        val btnCamRight = findViewById<ImageButton>(R.id.btnCamRight)

        btnForward.setOnTouchListener { v, event ->
            when (event.action) {
                MotionEvent.ACTION_DOWN -> {
                    mqttHelper.publish("comanda_masina", "FORWARD")

                    v.alpha = 0.6f
                    v.performClick()
                }
                MotionEvent.ACTION_UP -> {
                    mqttHelper.publish("comanda_masina", "STOP")
                    v.alpha = 1.0f
                    v.performClick()
                }
            }
            true
        }
        btnBackward.setOnTouchListener { v, event ->
            when (event.action) {
                MotionEvent.ACTION_DOWN -> {
                    mqttHelper.publish("comanda_masina", "BACKWARD")

                    v.alpha = 0.6f
                    v.performClick()
                }
                MotionEvent.ACTION_UP -> {
                    mqttHelper.publish("comanda_masina", "STOP")
                    v.alpha = 1.0f
                    v.performClick()
                }
            }
            true
        }
        btnLeft.setOnTouchListener { v, event ->
            when (event.action) {
                MotionEvent.ACTION_DOWN -> {
                    mqttHelper.publish("comanda_masina", "LEFT")

                    v.alpha = 0.6f
                    v.performClick()
                }
                MotionEvent.ACTION_UP -> {
                    mqttHelper.publish("comanda_masina", "STOP")
                    v.alpha = 1.0f
                    v.performClick()
                }
            }
            true
        }
        btnRight.setOnTouchListener { v, event ->
            when (event.action) {
                MotionEvent.ACTION_DOWN -> {
                    mqttHelper.publish("comanda_masina", "RIGHT")

                    v.alpha = 0.6f
                    v.performClick()
                }
                MotionEvent.ACTION_UP -> {
                    mqttHelper.publish("comanda_masina", "STOP")
                    v.alpha = 1.0f
                    v.performClick()
                }
            }
            true
        }

        btnCamUp.setOnTouchListener { v, event ->
            when (event.action) {
                MotionEvent.ACTION_DOWN -> {
                    mqttHelper.publish("control_camera", "UP")

                    v.alpha = 0.6f
                    v.performClick()
                }
                MotionEvent.ACTION_UP -> {
                    mqttHelper.publish("control_camera", "STOP")
                    v.alpha = 1.0f
                    v.performClick()
                }
            }
            true
        }
        btnCamDown.setOnTouchListener { v, event ->
            when (event.action) {
                MotionEvent.ACTION_DOWN -> {
                    mqttHelper.publish("control_camera", "DOWN")

                    v.alpha = 0.6f
                    v.performClick()
                }
                MotionEvent.ACTION_UP -> {
                    mqttHelper.publish("control_camera", "STOP")
                    v.alpha = 1.0f
                    v.performClick()
                }
            }
            true
        }
        btnCamLeft.setOnTouchListener { v, event ->
            when (event.action) {
                MotionEvent.ACTION_DOWN -> {
                    mqttHelper.publish("control_camera", "LEFT")

                    v.alpha = 0.6f
                    v.performClick()
                }
                MotionEvent.ACTION_UP -> {
                    mqttHelper.publish("control_camera", "STOP")
                    v.alpha = 1.0f
                    v.performClick()
                }
            }
            true
        }
        btnCamRight.setOnTouchListener { v, event ->
            when (event.action) {
                MotionEvent.ACTION_DOWN -> {
                    mqttHelper.publish("control_camera", "RIGHT")

                    v.alpha = 0.6f
                    v.performClick()
                }
                MotionEvent.ACTION_UP -> {
                    mqttHelper.publish("control_camera", "STOP")
                    v.alpha = 1.0f
                    v.performClick()
                }
            }
            true
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        mqttHelper.disconnect()
    }
}
