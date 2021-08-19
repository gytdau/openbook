import logo from "./logo.svg"
import "./App.scss"
import InlineTOC from "./InlineTOC"
import ChapterHeading from "./ChapterHeading"

function ChapterView(props) {
  let chapterId = props.chapterId
  let chapters = props.book.chapters
  return (
    <div className="container">
      <ChapterHeading chapterId={chapterId} chapters={chapters} />
      <div className="row">
        <div className="col-md-8 offset-md-2 calibre">
          <p class="p6">
            <span class="t14">
              You ask me, what is this General Bonaparte?...To know what he is,
              one would have to be he. Junot to his father,
            </span>{" "}
            1793
          </p>

          <p class="p6">
            FEW LIVES are as thoroughly documented as Napoleon’s. Yet aside from
            some general truths, little is known with certainty. Even the facts
            remain in dispute; his thoughts are enigmatic in their apparent
            contradictions; his intentions are mysterious. Napoleon himself
            foresaw this uncertainty, and he commented: “I would have found it
            very difficult to assert with any degree of truth what was my whole
            and real intention.”
          </p>

          <p class="p6">
            Indeed, why should a great man’s mind and soul be more transparent
            than those of the most humble and obscure? Who knows himself or
            others with true knowledge? The more we know of a man, the more
            numerous become the unanswered questions. And yet the impossibility
            of obtaining definitive answers should not discourage the
            questioner. As Napoleon remarked when young,{" "}
            <span class="t14">“Why</span> and <span class="t14">how</span> are
            such useful questions that they cannot be asked too often.”
          </p>

          <p class="p6">
            Our concern in this book is not with the acts of the man, or with
            his character or psychology, but with his thought and mind. Once
            expressed, thought is less mysterious than the thinker; the mystery
            is merely in the unexpressed residue. Spinoza is more easily
            understood than the village idiot. Unfortunately, between
            comprehending Spinoza’s philosophy and comprehending Spinoza’s mind
            there is a line that cannot be crossed. From his thought and from
            his manner of ordering it we can form some idea of his
            mind&mdash;but that is all.
          </p>

          <p class="p6">
            In the case of Napoleon or of the village idiot the situation is
            still more complex than with Spinoza, for no matter what they say,
            we still keep wondering what they <span class="t14">really</span>{" "}
            think; whereas with Spinoza, we may be reasonably sure that what he
            really thinks is precisely what he says. Let us now dismiss the
            idiot (though his presence was not irrelevant): what we have left is
            a philosopher, to whom thought is an end in itself, and a man of
            action, to whom thought is a means to an end. Philosophers are
            manipulators of thought; action is not their direct concern.
            Napoleon, no matter how deep his thought, was a manipulator of
            things and men. Hence his thought necessarily lacked that rounded,
            self-contained unity and harmonious order in which the philosopher
            rebuilds the universe and finds his peace. Like Margaret Fuller,
            Napoleon accepted the universe. He was at peace from the outset.
            Cosmic problems stimulated his fancy without causing him unrest.
            God, to him, was the solution of a socio-political problem, and in
            religion he saw “the mystery of the social order.”
          </p>

          <p class="p6">
            Such absence of system, such intellectual opportunism make
            Napoleon’s thought as a whole more difficult to understand than
            Spinoza’s. In Spinoza, each thought is a step to another thought; in
            Napoleon, each thought is a step to an action. In Spinoza, each step
            is difficult, demanding concentrated attention, but the view from
            the summit is bathed in the light of all-embracing recognition. In
            Napoleon, few individual thoughts are difficult to grasp. At their
            best, they afford deep insights&mdash;but never a panoramic vista.
            This is not to say that Napoleon’s thought lacks unity or coherence.
            Yet what unifying principle there is remains unstated, implicit,
            hence open to interpretation.
          </p>

          <p class="p6">
            In Spinoza’s philosophy, no thought on a given topic can be detached
            from the context of his whole thought without doing it violence. In
            Napoleon, each thought must be related not so much to the context of
            his other thoughts as to the context of his total activity. In many
            instances, it should also be related to the particular action on
            which it bears. By “total activity” we mean the total force of
            energy of which he was possessed. For it was the combination of his
            unique activity with his exceptional but by no means unique
            intellectual powers that made Napoleon what he was.
          </p>

          <p class="p6">
            Goethe said that Napoleon’s mind was the greatest the world had ever
            produced. He could not have based his judgment on what the Emperor
            said to him during their two interviews; both men said one or two
            profundities and many platitudes. No&mdash;what Goethe saw in
            Napoleon was a radiant power of the mind that cut through and
            dispelled the mists of speculation, strip ping all problems down to
            their simplest elements, discarding all obstacles to action:
          </p>

          <p class="p12">
            <span class="t15">“What centuries have dimly meditated</span>
          </p>

          <p class="p13">
            <span class="t15">His mind surveys in brightest clarity;</span>
          </p>

          <p class="p13">
            <span class="t15">All that is petty has evaporated,</span>
          </p>

          <p class="p14">
            <span class="t15">
              Here nothing is of weight save earth and sea.”
            </span>
          </p>

          <p class="p6">
            Such admiration is not surprising in the man who made Faust change
            the translation of John 1:1 from “In the beginning was the Word” to
            “In the beginning was the Deed.” Like the famed sun of Austerlitz,
            Napoleon’s mind stood solitary in a cloudless sky to light up naked
            action with its brightest rays.
          </p>

          <p class="p6">
            The present book, though it shows Napoleon’s mind in action, can
            afford only occasional glimpses of the active man. Even his mental
            activity is but fragmentarily revealed, for that activity was
            equally intense whether he spoke of questions of general human
            import or of trivial, practical, and ephemeral
            details&mdash;budgets, bookkeeping, fortifications, civil
            engineering, army rations, or the procurement of remounts. The
            reader has been spared such topics not merely because they are
            trivial and dull but chiefly because they acquire significance only
            in their totality. Yet those who take the time and trouble to survey
            the whole of Napoleon’s record will be rewarded with the insight
            that here was a man to whom nothing useful was trivial or dull. To
            the luminous strength of his mind, to its infinite power of
            concentration, there was no subject, no matter how arduous or
            remote, that could not be learned and conquered. If Napoleon had
            found it useful to learn Sanskrit, tightrope walking, and plumbing,
            he would have learned Sanskrit, tightrope walking, and
            plumbing&mdash;without an instant’s hesitation or fear. When we
            consider that virtually everything Napoleon knew he had picked up as
            he went along, we cannot help being awestruck: what we face here is
            not the divine spark but a dynamo.
          </p>

          <p class="p6">
            The utter fearlessness with which the young and inexperienced
            general addressed himself to problems seemingly beyond a single
            man’s scope characterizes the heroic element in Napoleon’s mind.
            There is something of a Hercules in it. Consider, for instance, how
            the thirty-year-old First Consul, within a few weeks after taking
            power, established a civil administration which proved to be the one
            and only stable political institution France has had in the past
            century and a half. There are those who see in Napoleon merely the
            military strong man, the dictator, just as Hercules is esteemed for
            his muscle rather than his brain. Yet exceptional mental powers are
            needed to devise a scheme as simple and bold as Hercules’ method of
            cleaning out the Augean stables: a graduate of an agricultural
            college would never have thought of it. Alexander’s handling of the
            Gordian knot may seem crude; Aristotle never taught him such a
            trick&mdash;but perhaps he learned it from Diogenes, the great
            simplifying Cynic.
          </p>

          <p class="p6">
            After 1805 or so, Napoleon’s mind gradually lost its heroic cast.
            Instead of approaching new problems with his usual fearless effort,
            he was content with capricious pronouncements that brooked no
            contradiction. Then came progressive disease, and with it spells of
            drowsy lethargy which in the end became almost continuous. “How I
            have fallen!” he exclaimed in 1820. “I, whose activity knew no
            limits, whose head never rested! I am plunged in a lethargic stupor,
            I must make an effort to raise my eyelids. Sometimes I used to
            dictate, on different subjects, to four or five secretaries who
            wrote as fast as I spoke. But I was Napoleon then; today I am
            nothing....I vegetate, I no longer live.” Yet even then, almost to
            his last breath, the old Napoleon revived as soon as his mind
            regained temporary strength. Then all became activity&mdash;dazzling
            conversation, furious gardening, tireless dictation. To his lucid
            mind, inaction was unbearable.
          </p>

          <p class="p6">
            This supreme combination of intellect and energy gave Napoleon’s
            mind a magnetic, almost supernatural power&mdash;a power that seems
            to radiate from his pictured features and endows his very name with
            magic. If modern times have produced a mythological figure, that
            figure is Napoleon. Abraham Lincoln is a possible rival, but as a
            figure of mythology Napoleon has a great advantage: like the
            Olympians, he is beyond good and evil, a true pagan god, eminently
            classical and Greek. Lincoln, a Christ-like figure from the
            backwoods, belongs to a different circle.
          </p>

          <p class="p6">
            Few men have expressed the Napoleon{" "}
            <span class="t14">mystique</span> so suggestively as Heine in these
            few sentences: “His countenance, too, was of the complexion we find
            on the marble heads of Greeks and Romans. The features were as nobly
            proportioned as those of ancient statues, and on his face was
            written: Thou shalt have no other god but me.”
          </p>

          <p class="p6">
            This <span class="t14">mystique</span> is not to be confused with
            the so-called Napoleonic legend, a political fabrication for which
            Napoleon himself is only partly responsible. Representing the
            Emperor as the champion of liberal and popular aspirations, the
            legend helped powerfully in placing Napoleon III on the throne and
            in keeping Bonapartism alive. It appealed to sentimentalists,
            chauvinists, and naive liberals, but it had nothing to do with the
            Napoleon <span class="t14">mystique</span> of less gullible
            men&mdash;Byron and Stendhal, for instance.
          </p>

          <p class="p6">
            Examined one by one, Napoleon’s accomplishments and utterances lose
            much of their magic. Their imperfections and errors, their
            improvised and derivative nature become only too apparent, and the
            man’s personal defects, his boundless egotism, deceitfulness, and
            callousness stand exposed. The sum of the parts is less than the
            whole. Unfortunately, this analytical “debunking,” if applied to
            almost any great man (with the possible exception of a handful of
            saints), would similarly divert attention from the majestic outline
            of the forest to the imperfection of the trees. A critical
            examination of a great man’s thought or deeds always leads to the
            ultimate, the only really important question: which is the deeper
            reality&mdash;the whole or the parts? If the answer is, the parts,
            then all greatness stands diminished. But before attempting to
            answer this question, let us return to Napoleon’s thought.
          </p>

          <p class="p6">
            The near-supernatural power of his mind, we have postulated, is a
            quality that has passed into his very name. To experience that
            power, no knowledge of his thought or deeds is necessary; simple
            imagination suffices. In fact, knowledge is a hindrance unless it is
            fairly extensive: then, by an effort of the mind, the scholar is
            able to apprehend something of the nature of the whole Napoleon and
            to understand rationally what is dimly sensed by the impressionable
            imagination.
          </p>

          <p class="p6">
            The collection of Napoleonic thoughts contained in this volume
            cannot give such an integral insight unless the reader is willing to
            make an effort of the imagination. On the contrary, it is more
            likely to furnish ammunition to the analytical critic. There is
            nothing wrong in this tendency; in fact, one of the purposes of this
            book is to show Napoleon at his best, at his worst, and in between.
            But some sort of corrective is needed to direct the reader’s
            attention to the essential coherence of Napoleon’s thought, a
            coherence which is present despite all the contradictions, despite
            the lack of system, despite the intellectual opportunism. The
            attempt at a synthesis in this Introduction does not concern itself
            with Napoleon’s views on individual topics&mdash;this would be a
            mere rehash&mdash;but with the general character of his thought.
          </p>
        </div>
      </div>
    </div>
  )
}

export default ChapterView
