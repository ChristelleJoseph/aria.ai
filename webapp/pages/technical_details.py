import streamlit as st
def show():
    # st.title("Recurrent Neural Network")

    # Sidebar for navigation
    st.sidebar.title("Navigation")

    section = st.sidebar.radio("Go to", ["Introduction(Inspiration)", "The Data", "The Model(RNN-LSTM)", "Future work"])

    st.markdown("""
            <style>
            .big-font {
                font-size:20px;
            }
            </style>
            """, unsafe_allow_html=True)

    # Conditional rendering of content based on sidebar navigation
    if section == "Introduction(Inspiration)":
        st.header("Drake feat. The Weekend")
        st.image('webapp/content_images/drakeWeekend.webp')
        st.markdown("""
                    <div class="big-font">
                    A while back, the music world was abuzz when a single purportedly by Drake hit the airwaves, encapsulating all the hallmark qualities of his music—catchiness and fire beats.
                    However, the twist in the tale was its true artist: not Drake, but an artificial intelligence.
                    While this revelation unsettled many, it sparked a profound fascination in me.
                    Having previously only considered AI in the realm of visual arts, the notion of its application to music was thrilling.
                    As an avid music enthusiast, this revelation ignited a curiosity within me to explore the possibilities of AI in music creation.
                    Thus began this passion project.</div>""", unsafe_allow_html=True)
        st.write("")



    elif section == "The Data":
        st.header("The Dataset")
        st.markdown("""

        <div class="big-font">
        I chose to work with an EDM dataset for two main reasons: firstly, my personal affinity for EDM, and secondly, because of EDM's repetitive nature.
        Repetition in music can facilitate the learning process for AI models by presenting clear, recurring musical elements and structures.


      https://cymatics.fm/products/odyssey-edm-sample-pack

        </div>""", unsafe_allow_html=True)



    elif section == "Long Short-Term Memory (LSTM) Networks":
        st.header("Long Short-Term Memory (LSTM) Networks")
        st.write("""
        LSTMs are a special kind of RNN capable of learning long-term dependencies. They were introduced by Hochreiter & Schmidhuber (1997) and have since been refined and popularized in various works.
        """)


    elif section == "Applications":
        st.header("Applications")
        st.write("""
        LSTMs are widely used for sequence prediction problems, such as time series prediction, natural language processing, speech recognition, and many more applications in areas where the sequence and context of data points are crucial.
        """)

footer="""<style>
.a {
    position: fixed;
    left: 0;
    bottom: 10px;
    width: 100%;
    background-color: white;
    color: black;
    text-align: center;
}
</style>
<div class="a">Made with ❤️ by Christelle J </div>
"""
st.markdown(footer,unsafe_allow_html=True)


# Make sure to call the show function
if __name__ == "__main__":
    show()
