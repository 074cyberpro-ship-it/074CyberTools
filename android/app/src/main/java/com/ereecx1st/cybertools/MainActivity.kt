package com.ereecx1st.cybertools

import android.app.Activity
import android.os.Bundle
import android.graphics.Color
import android.graphics.Typeface
import android.view.Gravity
import android.view.View
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.ScrollView

class MainActivity : Activity() {

    private val bg = Color.rgb(10, 12, 25)
    private val cyan = Color.rgb(0, 220, 255)
    private val white = Color.WHITE

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        window.statusBarColor = bg
        window.navigationBarColor = bg

        val root = LinearLayout(this)
        root.orientation = LinearLayout.VERTICAL
        root.setPadding(24, 30, 24, 24)
        root.setBackgroundColor(bg)

        val title = TextView(this)
        title.text = "074CyberTools"
        title.textSize = 28f
        title.setTextColor(cyan)
        title.setTypeface(null, Typeface.BOLD)
        root.addView(title)

        val subtitle = TextView(this)
        subtitle.text = "CYBER INTELLIGENCE PLATFORM"
        subtitle.textSize = 11f
        subtitle.setTextColor(white)
        root.addView(subtitle)

        val status = TextView(this)
        status.text = "\n● SYSTEM ONLINE"
        status.textSize = 14f
        status.setTextColor(Color.GREEN)
        root.addView(status)

        val scroll = ScrollView(this)
        val content = LinearLayout(this)
        content.orientation = LinearLayout.VERTICAL

        val modules = listOf(
            "HEALTH CHECK" to "Server monitoring",
            "IP INTELLIGENCE" to "IP information lookup",
            "DNS LOOKUP" to "Domain DNS records",
            "WORLD NEWS" to "Latest world headlines"
        )

        for ((name, description) in modules) {
            val card = LinearLayout(this)
            card.orientation = LinearLayout.VERTICAL
            card.setPadding(20, 22, 20, 22)
            card.setBackgroundColor(Color.rgb(23, 29, 49))

            val heading = TextView(this)
            heading.text = name
            heading.textSize = 17f
            heading.setTextColor(cyan)
            heading.setTypeface(null, Typeface.BOLD)

            val detail = TextView(this)
            detail.text = description
            detail.textSize = 13f
            detail.setTextColor(white)

            card.addView(heading)
            card.addView(detail)

            val params = LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
            )
            params.setMargins(0, 18, 0, 0)
            content.addView(card, params)
        }

        scroll.addView(content)
        root.addView(scroll)

        setContentView(root)
    }
}
