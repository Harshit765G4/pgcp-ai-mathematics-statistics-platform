"""Builds the initial curated question banks. Edit the QUESTION_ROWS section to add items."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
rows = []

def add(bank, topic, difficulty, kind, stem, options, answer, explanation, hint, wrong):
    assert len(options) == 4 and 0 <= answer < 4
    assert len(wrong) in (3, 4)
    prefix = {"core":"CORE", "practical":"PRACTICAL", "extension":"EXT"}[bank]
    bank_rows = [x for x in rows if x["bank"] == bank]
    n = len(bank_rows) + 1
    qid = f"{prefix}-{n:03d}"
    option_explanations = []
    wrong_iter = iter(wrong) if len(wrong) == 3 else None
    for i, option in enumerate(options):
        if i == answer:
            option_explanations.append("Correct. " + explanation)
        else:
            option_explanations.append(wrong[i] if len(wrong) == 4 else next(wrong_iter))
    # Deterministically rotate choices so correct answers are not always option A.
    shift = (sum(ord(ch) for ch in qid) + len(rows) * 3) % 4
    options = options[-shift:] + options[:-shift] if shift else options
    option_explanations = option_explanations[-shift:] + option_explanations[:-shift] if shift else option_explanations
    answer = (answer + shift) % 4
    rows.append({
        "id": qid,
        "number": len(rows) + 1,
        "bank": bank,
        "topicId": topic,
        "difficulty": difficulty,
        "type": kind,
        "question": stem,
        "options": options,
        "correctAnswer": answer,
        "explanation": explanation,
        "optionExplanations": option_explanations,
        "hint": hint,
        "referenceId": topic + "-ref"
    })

# ------------------------------ CORE SYLLABUS ------------------------------
# AI fundamentals
add('core','ai-foundations','basic','concept','Which statement best captures the scope of Artificial Intelligence?',
    ['The study of systems that perceive, reason, learn, plan or act toward goals','The process of storing every possible input in a fixed lookup table','The exclusive use of neural networks to classify images','The automation of physical machinery without information processing'],0,
    'AI is a broad field concerned with intelligent capabilities such as perception, reasoning, learning, planning and action. Neural networks are one family of techniques, not the whole field.',
    'Think of AI as a collection of capabilities and methods, not one particular model.',
    ['A lookup table is one possible implementation technique and does not define the field.','Neural networks are important but do not exhaust symbolic, search-based or other AI approaches.','Physical automation can be non-intelligent and is not the defining boundary of AI.'])
add('core','ai-history','basic','concept','What is the primary purpose of an abstract Turing Machine?',
    ['To provide a mathematical model of computation','To determine whether a chatbot is conscious','To imitate a biological neuron using voltages','To rank web pages by relevance'],0,
    'A Turing Machine is a formal model consisting of a tape, a read/write head, states and transition rules. It is used to reason about computability.',
    'Separate the theoretical model of computation from the conversational imitation game.',
    ['Consciousness is not what the Turing Machine formalises.','A biological neuron model is a different modelling idea.','Ranking web pages is an information-retrieval task, not the definition of a Turing Machine.'])
add('core','ai-history','medium','concept','In the Turing Test as described in the syllabus, what is the evaluator primarily judging?',
    ['Whether the system can be distinguished from a human through its responses','Whether the system has a biological body','Whether the system uses a neural network internally','Whether the system can solve every mathematical problem'],0,
    'The imitation-game setup asks whether a judge can reliably distinguish machine and human responses in the specified interaction. It does not directly establish consciousness or universal competence.',
    'Focus on the observable interaction and the evaluator’s judgement.',
    ['A biological body is not required in the text-based imitation-game framing.','The internal architecture is not the criterion being judged.','The test does not require solving every mathematical problem.'])
add('core','ai-history','medium','concept','A simulated colony forms organised trails even though each virtual agent follows only local rules. Which concept does this illustrate?',
    ['Emergent behaviour','Matrix inversion','Predicate quantification','Supervised labelling'],0,
    'Emergent behaviour is a system-level pattern produced by interactions among simpler components, rather than a central instruction specifying the overall pattern.',
    'Look for a global pattern arising from local interactions.',
    ['Matrix inversion is an algebraic operation and does not explain the colony pattern.','Predicate quantification is a logic concept, not collective organisation.','Supervised labelling concerns learning from target labels.'])
add('core','ai-ethics','medium','scenario','A model has high overall accuracy but produces substantially more false rejections for one demographic group. Which responsible-AI concern is most directly raised?',
    ['Fairness and disparate impact','Matrix orthogonality','Search completeness','Vector normalisation'],0,
    'A strong aggregate score can hide uneven error rates across groups. Fairness assessment requires examining relevant subgroup outcomes and the deployment context.',
    'Disaggregate performance instead of relying only on the overall average.',
    ['Orthogonality is a geometric property of vectors or matrices.','Search completeness concerns whether a search method finds a solution when one exists.','Vector normalisation changes vector scale and does not address group error disparities.'])
add('core','ai-ethics','medium','concept','Why is meaningful human oversight more than simply placing a person’s name on an AI approval form?',
    ['The reviewer needs information, authority and a practical opportunity to intervene','The reviewer must always accept the model’s recommendation','The reviewer must be able to retrain the model from memory','The reviewer removes the need for monitoring after deployment'],0,
    'Oversight is meaningful only when people can understand relevant limitations, have authority to challenge or override outcomes, and have enough time and process support to act.',
    'Ask whether the human can actually detect and correct a problem.',
    ['Automatic acceptance is not oversight.','Retraining from memory is not a necessary or sufficient oversight condition.','Monitoring remains important because inputs, users and risks can change after deployment.'])
add('core','ai-systems','basic','concept','In a typical expert-system architecture, where are domain facts and IF–THEN rules stored?',
    ['Knowledge base','Inference engine','User interface only','Output actuator'],0,
    'The knowledge base stores domain knowledge such as facts, rules and relationships. The inference engine applies that knowledge to derive conclusions.',
    'Distinguish stored domain knowledge from the mechanism that reasons over it.',
    ['The inference engine applies rules rather than serving as the rule repository.','A user interface presents information; it is not the whole knowledge store.','An actuator carries out actions and is not the knowledge repository.'])
add('core','ai-systems','medium','concept','A rule system starts with known facts and repeatedly fires every rule whose conditions match, adding new facts. Which reasoning direction is being used?',
    ['Forward chaining','Backward chaining','Adversarial search','Singular value decomposition'],0,
    'Forward chaining is data-driven: it begins with known facts and derives consequences by applying matching rules.',
    'The process moves from facts toward conclusions.',
    ['Backward chaining starts from a goal and seeks supporting premises.','Adversarial search reasons about competing agents and game outcomes.','SVD is a matrix factorisation technique.'])
add('core','ml-learning','basic','concept','A dataset contains customer attributes but no target categories. The goal is to discover groups of similar customers. Which learning paradigm fits?',
    ['Unsupervised learning','Supervised classification','Supervised regression','Reinforcement learning with a supplied reward sequence'],0,
    'Clustering is an unsupervised task because the training data do not include predefined target labels; the method seeks structure in the inputs.',
    'Check whether examples come with known target labels.',
    ['Classification requires labelled categories.','Regression requires numerical target values.','The scenario does not describe sequential actions and rewards.'])
add('core','ml-learning','basic','concept','Predicting the selling price of a house from its features is most naturally framed as:',
    ['Supervised regression','Unsupervised clustering','Adversarial search','Predicate-logic resolution'],0,
    'Historical examples with known prices provide numerical targets, making the task supervised regression.',
    'The output is a number learned from labelled examples.',
    ['Clustering groups examples without supplied target prices.','Adversarial search handles opposing objectives, commonly in games.','Resolution is a logical inference method, not a price-prediction paradigm.'])
add('core','knowledge-representation','medium','concept','Which set of elements most completely defines a classical state-space search problem?',
    ['Initial state, actions, transition model, goal test and path cost','Only an initial state and a list of possible answers','Training labels, validation labels and a loss function','A covariance matrix, eigenvalues and singular values'],0,
    'A standard search formulation specifies where the search starts, what actions are available, how actions change states, how goals are recognised and how path costs are assessed.',
    'Think of what an algorithm needs to generate successors and recognise a solution.',
    ['A list of answers omits the transition and goal structure.','These are elements of supervised model development, not state-space search.','These are linear-algebra and statistical quantities, not a complete search definition.'])
add('core','knowledge-representation','medium','concept','In a route-finding problem, what is the role of the transition model?',
    ['It describes the resulting city or state after taking a road from the current city','It checks only whether the destination has been reached','It assigns the final grade to the search algorithm','It stores the heuristic estimate without describing actions'],0,
    'The transition model specifies how an action changes the current state, for example moving from one city to an adjacent city.',
    'Ask what changes when an action is applied.',
    ['The goal test checks destination satisfaction.','Evaluation may assess an algorithm but is not the transition model.','A heuristic may estimate distance, but it does not replace the state transition definition.'])
add('core','search','medium','concept','Which frontier data structure is conventionally used by breadth-first search?',
    ['First-in, first-out queue','Last-in, first-out stack','Priority queue ordered by estimated heuristic only','Hash table ordered by vector norm'],0,
    'BFS expands the shallowest nodes first, which is implemented with a FIFO queue.',
    'The earliest generated frontier node is expanded first.',
    ['A stack is associated with depth-first search.','A heuristic-only priority queue is typical of greedy best-first search, not standard BFS.','Vector norm is unrelated to the standard BFS frontier discipline.'])
add('core','search','medium','concept','For a finite branching search tree with equal step costs, which statement about BFS is correct?',
    ['It is complete and finds a shallowest, hence lowest-step-count, solution','It always uses less memory than DFS','It is optimal even when step costs vary arbitrarily','It can only search trees with exactly two successors per node'],0,
    'BFS is complete under finite branching and finds a shallowest goal. With equal step costs, a shallowest solution also has minimum path cost.',
    'The equal-cost condition is important for the optimality claim.',
    ['BFS often uses more memory than DFS because it stores a broad frontier.','When step costs differ, shallowest need not mean cheapest.','BFS is not restricted to binary branching.'])
add('core','search','medium','concept','What is a common limitation of depth-first search in a search space with an infinite-depth branch?',
    ['It may follow that branch indefinitely without reaching a solution elsewhere','It must store every node at the current depth before proceeding','It always returns a minimum-cost solution','It cannot be implemented recursively'],0,
    'DFS may become trapped on a deep or infinite branch and fail to explore another branch containing a goal. It is memory-efficient in many tree settings but not generally complete in infinite-depth spaces.',
    'Consider what happens if the first branch never ends.',
    ['Storing an entire breadth frontier is more characteristic of BFS.','DFS is not generally cost-optimal.','Recursive DFS is a common implementation, though an explicit stack is also possible.'])
add('core','search','medium','concept','When road segments have different non-negative costs and the goal is the least-cost route, which uninformed strategy is appropriate?',
    ['Uniform-cost search','Depth-first search','Breadth-first search by depth alone','A random walk with no cost tracking'],0,
    'Uniform-cost search expands the frontier path with the smallest accumulated path cost and is optimal under standard non-negative cost conditions.',
    'The algorithm must compare total cost so far, not merely number of edges.',
    ['DFS does not systematically prioritise least accumulated cost.','BFS by depth is optimal only when step costs are equal.','A random walk does not guarantee least-cost exploration.'])
add('core','search','medium','concept','In minimax search, how does a MIN node select its backed-up value?',
    ['It selects the minimum of its child values','It selects the maximum of its child values','It averages all child values regardless of the game model','It chooses the child with the largest branching factor'],0,
    'MIN represents the opponent choosing the outcome least favourable to MAX, so it backs up the minimum child value.',
    'The node name tells you whose objective is being optimised.',
    ['The maximum is selected at MAX nodes.','Averaging is not the minimax rule.','Branching factor does not determine the minimax utility.'])
add('core','agents-csp','basic','concept','Which description best defines an intelligent agent?',
    ['A system that perceives its environment and selects actions','A database that stores only historical observations','A function that must always return the same output for every input','A matrix with orthonormal columns'],0,
    'An agent receives percepts from an environment and selects actions that affect the environment, often guided by a performance measure.',
    'Look for the perception–action cycle.',
    ['A database may support an agent but does not itself define agency.','A deterministic function can vary with its input; identical output for all inputs is not required.','Orthonormal columns describe a matrix property.'])
add('core','agents-csp','medium','concept','A constraint-satisfaction problem is conventionally described by which three components?',
    ['Variables, domains and constraints','Agents, sensors and actuators only','States, rewards and discount factors only','Rows, columns and eigenvalues'],0,
    'A CSP contains variables to assign, a domain of possible values for each variable and constraints that restrict allowed combinations.',
    'List what needs a value, what values are allowed and what makes assignments compatible.',
    ['Sensors and actuators describe agent interaction but not the standard CSP triple.','Rewards and discount factors describe reinforcement-learning settings.','Rows, columns and eigenvalues are matrix concepts.'])
add('core','logic','medium','concept','Which formula expresses “Every student submitted an assignment” using Student(x) and Submitted(x)?',
    ['∀x (Student(x) → Submitted(x))','∃x (Student(x) ∧ Submitted(x))','∀x (Student(x) ∧ ¬Submitted(x))','∃x (Student(x) → ¬Submitted(x))'],0,
    'The universal statement applies to every object in the domain: if an object is a student, it has submitted. The implication avoids requiring every domain object to be a student.',
    'Use a universal quantifier and an implication from being a student to having submitted.',
    ['This says at least one object is both a student and a submitter.','This says every object is a student and has not submitted, which is much stronger and opposite.','This is existential and does not express that all students submitted.'])
add('core','logic','medium','concept','For material implication P → Q, in which case is the statement false?',
    ['P is true and Q is false','P is false and Q is false','P is false and Q is true','P is true and Q is true'],0,
    'Material implication is false only when the antecedent is true but the consequent is false; in all other truth-value combinations it is true.',
    'The one failing case is a promise whose condition happened but whose consequence did not.',
    ['When P is false, the implication is true under material implication.','A false antecedent makes the implication true.','A true antecedent and true consequent satisfy the implication.'])
add('core','reasoning-planning','hard','concept','Given clauses (A ∨ P) and (B ∨ ¬P), which resolvent follows by resolving on P?',
    ['A ∨ B','A ∧ B','P ∨ ¬P','¬A ∨ ¬B'],0,
    'Resolution removes the complementary pair P and ¬P and combines the remaining literals, producing A ∨ B.',
    'Remove the complementary literals and keep the other literal from each clause.',
    ['Conjunction is not the resolution operation; the result is a clause.','P ∨ ¬P is a tautology and is not the resolvent of these clauses.','Negating the remaining literals is not part of resolution.'])
add('core','reasoning-planning','medium','concept','In classical planning, what does an action precondition specify?',
    ['What must be true before the action can be applied','What must be true after every possible plan has ended','The numerical learning rate of the planner','The final score of a search engine'],0,
    'A precondition is a set of conditions that must hold in the current state before the action is legal. Effects describe how the state changes.',
    'Separate conditions before an action from changes caused by the action.',
    ['Postconditions or effects describe changes after application, not preconditions.','A learning rate belongs to optimisation.','Search-engine scoring is unrelated to action applicability.'])
add('core','big-data','basic','concept','Which example is most clearly unstructured data in the usual database-schema sense?',
    ['A free-form customer review paragraph','A table with fixed columns for customer ID and purchase date','A relational table of product IDs and integer quantities','A CSV file with consistent rows and named fields'],0,
    'Free-form text does not follow a fixed relational tabular schema, so it is conventionally treated as unstructured data.',
    'Look for the item without predefined columns and typed fields.',
    ['A fixed-column table is structured.','A relational table is structured.','A consistently tabular CSV is structured even though it is stored as a text file.'])
add('core','big-data','medium','concept','Which “V” of big data refers to the speed at which data are generated, arrive or need to be processed?',
    ['Velocity','Variety','Volume','Veracity'],0,
    'Velocity is about the rate of data generation, arrival and processing. Volume is amount, variety is diversity of forms, and veracity concerns quality or trustworthiness.',
    'Think of data arriving rapidly from live sensors or transactions.',
    ['Variety concerns formats and sources.','Volume concerns total amount.','Veracity concerns data quality and reliability.'])

# Linear algebra core
add('core','vectors','basic','concept','What is the result type of the standard dot product of two real vectors of equal length?',
    ['A scalar','A vector with the same dimension','A square matrix','A Boolean value indicating equality'],0,
    'The dot product sums pairwise component products and returns one scalar value.',
    'The operation combines all component products into one number.',
    ['A vector result is associated with operations such as vector addition or cross product in 3D.','A matrix result is associated with outer products.','The dot product is not merely an equality test.'])
add('core','vectors','medium','concept','For non-zero vectors a and b, what does a·b = 0 imply in ordinary Euclidean space?',
    ['The vectors are orthogonal','The vectors have equal lengths','The vectors point in exactly the same direction','The vectors must both be unit vectors'],0,
    'A zero dot product means the vectors are perpendicular (orthogonal) in Euclidean geometry. It does not determine their lengths.',
    'Use the geometric relation a·b=||a||||b||cosθ.',
    ['Orthogonality does not require equal norms.','Same-direction non-zero vectors have a positive dot product.','Unit length is not implied by a zero dot product.'])
add('core','vectors','medium','concept','Cosine similarity is most directly intended to compare which property of two non-zero vectors?',
    ['Their angular orientation, independent of positive scaling','Their Euclidean distance including magnitude','Their number of non-zero coordinates only','The determinant of the matrix formed by their entries'],0,
    'Cosine similarity divides the dot product by the product of the norms, normalising away magnitude and measuring the angle between vectors.',
    'Notice that both vector norms appear in the denominator.',
    ['Euclidean distance includes magnitude differences.','The count of non-zero coordinates is not the cosine formula.','The determinant is defined for a square matrix, not this pairwise similarity definition.'])
add('core','vector-spaces','medium','concept','A set of vectors is linearly independent when:',
    ['Only the trivial coefficient choice makes their linear combination equal zero','At least one vector is a scalar multiple of another','Their span contains the zero vector only','Every vector has unit Euclidean norm'],0,
    'Independence means c₁v₁+…+cₖvₖ=0 has only c₁=…=cₖ=0 as a solution.',
    'Set the linear combination equal to the zero vector and inspect its coefficients.',
    ['A scalar-multiple relationship creates dependence.','The span of any non-empty vector set includes the zero vector.','Unit norms do not determine independence.'])
add('core','vector-spaces','medium','concept','What two properties must a basis of a finite-dimensional vector space satisfy?',
    ['It spans the space and is linearly independent','It contains the zero vector and is orthogonal','It has the largest possible number of vectors, including repetitions','It consists only of vectors with positive entries'],0,
    'A basis is a minimal spanning set, equivalently a spanning set that is linearly independent.',
    'A basis must be able to generate the whole space without redundancy.',
    ['A basis cannot contain the zero vector because that creates dependence.','Repeated or redundant vectors violate independence.','Positive entries are not required; basis vectors may contain negative or zero entries.'])
add('core','vector-spaces','basic','concept','What is the dimension of ℝ⁴?',
    ['4','2','8','It depends on the values of the vector coordinates'],0,
    'The standard basis of ℝ⁴ contains four independent coordinate vectors, so its dimension is four.',
    'Dimension is the number of vectors in a basis, not the number of possible points.',
    ['Two is not the number of independent coordinate directions in ℝ⁴.','Eight is unrelated to its basis size.','Dimension is a property of the space, not of a particular vector’s coordinate values.'])
add('core','linear-maps','medium','concept','Which property must every linear map T satisfy?',
    ['T(0)=0','T(0)=b for any non-zero translation vector b','T(u+v)=T(u)T(v) using scalar multiplication','T(cu)=T(u)+c for every scalar c'],0,
    'Linearity implies homogeneity and additivity; setting c=0 in homogeneity gives T(0)=0.',
    'Apply the scalar-multiplication property with scalar zero.',
    ['A nonzero translation generally makes a transformation affine rather than linear.','Linearity preserves vector addition, not multiplication of vectors.','The homogeneity property is T(cu)=cT(u).'])
add('core','linear-maps','medium','concept','A linear transformation maps ℝ⁵ into ℝ³. What is the maximum possible rank of its matrix?',
    ['3','5','8','15'],0,
    'Rank cannot exceed either the number of rows (3) or columns (5), so the maximum is min(3,5)=3.',
    'Rank is bounded by the smaller matrix dimension.',
    ['The matrix has only three output coordinates, so rank cannot be five.','Eight is larger than either dimension.','The product of the dimensions is not a rank bound.'])
add('core','matrices','basic','concept','If A is 2×3 and B is 3×4, what is the shape of AB?',
    ['2×4','3×3','4×2','2×3'],0,
    'The inner dimensions 3 and 3 match, and the product keeps the outer dimensions, giving 2×4.',
    'For an m×n matrix multiplied by n×p, the result is m×p.',
    ['3×3 does not preserve the outer dimensions.','4×2 would correspond to a different product order and dimensions.','2×3 is the shape of A, not the product.'])
add('core','matrices','medium','concept','Which identity correctly describes the transpose of a product?',
    ['(AB)ᵀ = BᵀAᵀ','(AB)ᵀ = AᵀBᵀ','(AB)ᵀ = AB','(AB)ᵀ = A⁻¹B⁻¹ for every A and B'],0,
    'The transpose reverses product order: (AB)ᵀ=BᵀAᵀ. The identity is essential in matrix calculus and linear algebra.',
    'Transpose the factors and reverse their order.',
    ['This keeps the order unchanged and is generally wrong.','The transpose of a product is not generally the same product.','Inverses may not exist and are not the transpose rule.'])
add('core','matrices','medium','concept','For a square matrix A, which condition is equivalent to A being invertible?',
    ['det(A) ≠ 0','det(A) = 0','Every entry of A is non-zero','A has at least one zero eigenvalue'],0,
    'A square matrix is nonsingular exactly when its determinant is non-zero; equivalently, its columns are independent and its inverse exists.',
    'Recall the determinant test for singularity.',
    ['A zero determinant means singular, not invertible.','Entry-wise nonzero values do not guarantee nonsingularity.','A zero eigenvalue implies singularity.'])
add('core','matrices','medium','concept','What distinguishes the Hadamard product from ordinary matrix multiplication?',
    ['It multiplies corresponding entries element by element','It computes row-by-column dot products','It requires the left matrix to be square and invertible','It always produces a scalar'],0,
    'The Hadamard product multiplies entries at matching positions and normally requires equal-shaped matrices. Standard matrix multiplication combines rows and columns.',
    'Think of matching positions rather than row–column dot products.',
    ['Row-by-column dot products define standard matrix multiplication.','Invertibility is not required for an element-wise product.','The Hadamard product returns a matrix of the same shape.'])
add('core','matrix-properties','medium','concept','For a real orthogonal square matrix Q, which statement is true?',
    ['Q⁻¹ = Qᵀ','Q⁻¹ = −Qᵀ for every Q','QᵀQ = 0','Q must be diagonal'],0,
    'Orthogonality means QᵀQ=I, so Qᵀ is the inverse. Orthogonal transformations preserve Euclidean lengths and angles.',
    'Use the defining equation QᵀQ=I.',
    ['The inverse is the transpose, without a negative sign.','QᵀQ equals the identity, not the zero matrix.','Rotations can be orthogonal without being diagonal.'])
add('core','matrix-properties','medium','concept','A real symmetric matrix A is positive definite when:',
    ['xᵀAx > 0 for every non-zero real vector x','Every entry of A is strictly positive','All row sums are equal','A is necessarily the identity matrix'],0,
    'Positive definiteness is defined through the quadratic form xᵀAx being positive for all non-zero x. It is a global algebraic condition, not an entry-wise condition.',
    'Use the quadratic form definition.',
    ['Positive-definite matrices can contain negative off-diagonal entries.','Positive entries alone do not ensure positive definiteness.','Equal row sums are not the definition.','The identity is positive definite, but it is only one example.'])
add('core','matrix-properties','basic','concept','What is the trace of a square matrix?',
    ['The sum of its main-diagonal entries','The product of all its entries','The number of non-zero rows','The sum of all singular values for every matrix'],0,
    'The trace is the sum of diagonal entries of a square matrix. It is also equal to the sum of eigenvalues counted with algebraic multiplicity.',
    'Look only at the main diagonal.',
    ['The product of all entries is not the trace.','Rank relates to independent rows or columns, not trace.','The sum of singular values is the nuclear norm and is not generally the trace.'])
add('core','eigen-pca-svd','medium','concept','Which equation defines an eigenvector v and eigenvalue λ of a square matrix A?',
    ['Av = λv, where v is non-zero','Av = 0 for every vector v','A + v = λI','Aᵀv = λ for any scalar λ'],0,
    'An eigenvector is a non-zero direction that the transformation maps to a scalar multiple of itself. The scalar is the corresponding eigenvalue.',
    'The transformed vector must remain on the same line as v.',
    ['Av=0 describes a null-space vector and would correspond only to eigenvalue zero if v is nonzero.','The addition equation is not the eigenvector definition.','The right-hand side should be a vector λv, not an arbitrary scalar.'])
add('core','eigen-pca-svd','medium','concept','Why are eigenvectors especially useful in understanding a real symmetric matrix?',
    ['It has an orthonormal basis of eigenvectors','Its eigenvalues must all be negative','Its eigenvectors are always identical to the coordinate axes','It cannot be diagonalised'],0,
    'The spectral theorem states that a real symmetric matrix is orthogonally diagonalizable, with an orthonormal eigenbasis and real eigenvalues.',
    'Recall the spectral theorem for real symmetric matrices.',
    ['Symmetric matrices may have positive, negative or zero eigenvalues.','Eigenvectors need not align with the original coordinate axes.','Real symmetric matrices are diagonalizable by an orthogonal matrix.'])
add('core','eigen-pca-svd','medium','concept','In PCA, what do the leading principal components represent?',
    ['Directions that capture the greatest variance in the data, in descending order','The original feature columns sorted alphabetically','Directions with the smallest possible variance first','The class labels that supervise a classifier'],0,
    'PCA finds orthogonal directions of maximal variance in centred data; components are linear combinations of original features.',
    'Think about the variance captured by each projected direction.',
    ['Principal components are not simply alphabetically ordered input columns.','The first component maximises variance rather than minimising it.','PCA is ordinarily an unsupervised dimensionality-reduction method and does not require class labels.'])
add('core','eigen-pca-svd','medium','concept','Which property is guaranteed for singular values in an SVD?',
    ['They are non-negative','They are always equal to the eigenvalues of A','They must be negative for a rank-deficient matrix','There is one singular value for every entry of A'],0,
    'In A=UΣVᵀ, singular values are the non-negative diagonal entries of Σ, usually ordered from largest to smallest.',
    'The SVD diagonal matrix contains lengths/scales, not signed eigenvalues.',
    ['Singular values are non-negative by definition.','For non-square or nonsymmetric A, singular values are not generally eigenvalues of A.','Rank deficiency creates zero singular values, not negative ones.','The number of singular values is bounded by min(m,n), not the number of entries.'])

# Calculus core
add('core','derivatives','basic','concept','Geometrically, what does f′(a) represent when the derivative exists?',
    ['The slope of the tangent to y=f(x) at x=a','The total area under f from 0 to a','The function value at x=a','The average slope over the entire domain'],0,
    'The derivative is the instantaneous rate of change and equals the tangent-line slope at the point for a differentiable graph.',
    'Distinguish instantaneous slope from accumulated area or average change.',
    ['Area is associated with integration.','The function value is f(a), not f′(a).','An average slope uses a finite interval, not an instantaneous limit.'])
add('core','derivatives','medium','concept','Which rule is needed to differentiate f(x)=u(x)v(x)?',
    ['Product rule: (uv)′=u′v+uv′','Chain rule only: (uv)′=u′v′','Quotient rule: (uv)′=(u′v−uv′)/v²','Power rule only, regardless of u and v'],0,
    'The derivative of a product is the derivative of the first factor times the second plus the first times the derivative of the second.',
    'Each factor is differentiated once while the other is kept unchanged.',
    ['Differentiating both factors and multiplying their derivatives is not the product rule.','The quotient rule applies to a ratio, not a product.','The power rule alone is not sufficient for arbitrary functions u and v.'])
add('core','derivatives','medium','concept','Which statement about differentiability and continuity is mathematically correct?',
    ['Differentiability at a point implies continuity there','Continuity always implies differentiability','A function is differentiable only when its derivative is positive','A zero derivative means the function is discontinuous'],0,
    'A differentiable function is continuous at the point, but a continuous function may have a corner or other non-differentiable behaviour.',
    'The implication works in one direction only.',
    ['A continuous function such as |x| at zero is not differentiable there.','The derivative may be negative or zero as well as positive.','A zero derivative is compatible with a smooth constant function.'])
add('core','multivariable','medium','concept','When calculating ∂f/∂x for f(x,y), what is done with y?',
    ['It is treated as constant during differentiation with respect to x','It is set equal to zero in every problem','It is differentiated with respect to x as well','It is replaced with the derivative of x'],0,
    'A partial derivative differentiates with respect to one chosen variable while holding the other independent variables fixed.',
    'The symbol ∂/∂x tells you which variable changes.',
    ['Setting y=0 changes the problem and is not the definition.','Differentiating y with respect to x is not part of the partial derivative when x and y are independent.','There is no rule replacing y with a derivative of x.'])
add('core','multivariable','medium','concept','For a differentiable scalar function f, which direction gives the greatest instantaneous rate of increase at a point where ∇f is non-zero?',
    ['The direction of the gradient','The direction opposite to the gradient','Any direction tangent to a level set','A direction perpendicular to the gradient'],0,
    'The directional derivative along a unit vector u is ∇f·u, which is maximised when u points in the direction of ∇f.',
    'Use the dot product and its maximum when two vectors align.',
    ['The negative gradient gives the steepest decrease.','A tangent direction to a level set has zero first-order change.','A perpendicular direction also gives zero directional derivative.'])
add('core','gradients-autodiff','medium','concept','What does backpropagation compute in a neural network?',
    ['Gradients of a loss with respect to intermediate values and parameters','The class labels for the training set','The global minimum without an optimiser','The exact inverse of every weight matrix'],0,
    'Backpropagation efficiently applies the chain rule through a computational graph to obtain gradients. An optimiser then uses these gradients to update parameters.',
    'Separate derivative computation from the parameter-update rule.',
    ['Labels are part of the training targets, not computed by backpropagation.','Gradient calculation alone does not guarantee finding a global minimum.','Backpropagation does not invert weight matrices.'])
add('core','gradients-autodiff','medium','concept','Which statement best distinguishes automatic differentiation from finite differences?',
    ['Automatic differentiation applies chain rules to elementary operations; finite differences approximate derivatives using function evaluations','Automatic differentiation always requires symbolic algebra; finite differences never evaluate the function','Finite differences are exact for every smooth function','Automatic differentiation and numerical finite differences are identical methods'],0,
    'Automatic differentiation propagates derivatives through a computational graph using exact local derivative rules (up to floating-point arithmetic). Finite differences estimate slopes from nearby function values.',
    'Look at whether derivatives are propagated through operations or estimated from small input changes.',
    ['Automatic differentiation does not require a symbolic closed-form expression.','Finite differences evaluate the function at perturbed inputs.','Finite-difference estimates generally have truncation and rounding error.','The methods have different mechanisms and error properties.'])
add('core','gradients-autodiff','hard','concept','For a smooth scalar function near a point a, what does the first-order Taylor approximation provide?',
    ['A local linear approximation using the function value and gradient at a','An exact representation of every nonlinear function over the whole domain','The covariance matrix of the input data','The list of all stationary points'],0,
    'The first-order approximation is f(a+h)≈f(a)+∇f(a)ᵀh for small h. Higher-order terms capture curvature and approximation error.',
    'It is a local approximation based on first derivatives.',
    ['A nonlinear function is not generally represented exactly by one linear expression.','Covariance is a statistical quantity, not the Taylor approximation.','The expression approximates nearby values; it does not enumerate stationary points.'])
add('core','optimization','medium','concept','For minimisation, which is the standard gradient-descent update?',
    ['xₖ₊₁ = xₖ − η∇f(xₖ)','xₖ₊₁ = xₖ + η∇f(xₖ)','xₖ₊₁ = ηxₖ − ∇f(xₖ)','xₖ₊₁ = xₖ − ηf(xₖ)'],0,
    'The negative gradient points in the local direction of steepest decrease. The learning rate η controls the step size.',
    'A minimisation step moves opposite to the gradient.',
    ['This moves uphill for a sufficiently small positive learning rate.','This scales the current point and subtracts a scalar function value, not the gradient vector.','The update subtracts the gradient, not the objective value itself.'])
add('core','optimization','medium','concept','In equality-constrained optimisation, what is the main role of a Lagrange multiplier?',
    ['To incorporate a constraint into stationary-point equations through the Lagrangian','To guarantee that every stationary point is a global minimum','To replace the objective function with a random search','To make the constraint disappear from the problem'],0,
    'The Lagrangian combines the objective with equality constraints, and its stationary conditions help locate constrained optima under appropriate regularity conditions.',
    'The multiplier is attached to a constraint equation.',
    ['A stationary point may be a maximum or saddle, and global guarantees need further assumptions.','Lagrange multipliers are analytical conditions, not random search.','The constraint remains central to the Lagrangian equations.'])
add('core','optimization','medium','concept','What is a key property of a differentiable convex objective on a convex feasible set?',
    ['Every local minimum is also a global minimum','Every stationary point must be a strict maximum','It has exactly one stationary point','Its Hessian must be the identity matrix'],0,
    'Convexity rules out nonglobal local minima. A minimiser, when one exists, is global; uniqueness requires stronger conditions such as strict convexity.',
    'Convexity concerns the shape of the objective and the relationship between local and global minima.',
    ['A convex function does not have local maxima in the general interior sense unless it is constant in relevant directions.','There may be many stationary points or none in an unconstrained domain.','The Hessian need only be positive semidefinite where the twice-differentiable convexity condition applies, not identity.'])
add('core','vector-matrix-calculus','medium','concept','For f: ℝⁿ → ℝᵐ, using the output-by-input convention, what is the shape of its Jacobian?',
    ['m×n','n×m','n×n for all m','m×m for all n'],0,
    'Each row corresponds to an output component and each column to an input variable, so Jᵢⱼ=∂fᵢ/∂xⱼ has shape m×n.',
    'Count output components for rows and input variables for columns.',
    ['This is the transpose convention, not the output-by-input convention specified.','The Jacobian need not be square.','The Jacobian need not be square.'])
add('core','vector-matrix-calculus','hard','concept','A scalar-valued function f: ℝⁿ → ℝ has what Jacobian shape under the output-by-input convention?',
    ['1×n','n×1','n×n','1×1 for every n'],0,
    'There is one output component and n input variables, so the Jacobian is a row with n partial derivatives. Many texts represent the gradient as an n×1 column; the convention must be checked.',
    'The output count is one; the input count is n.',
    ['This is the common column-gradient representation, not the Jacobian convention stated in the question.','An n×n Hessian is a second-derivative object.','The Jacobian contains one partial derivative per input variable.'])
add('core','optimization-algorithms','medium','concept','The function f(x,y)=x²−y² has a stationary point at (0,0). How should this point be classified?',
    ['Saddle point','Strict local minimum','Strict local maximum','Point where the gradient does not exist'],0,
    'The gradient is zero at the origin. Along the x direction the function increases away from zero, while along the y direction it decreases, so the point is a saddle.',
    'Compare the function along the x-axis and y-axis near the origin.',
    ['Along the y-axis, f(0,y)=−y²<0, so nearby values are lower.','Along the x-axis, f(x,0)=x²>0, so nearby values are higher.','The function is a polynomial, so its gradient exists everywhere.'])
add('core','optimization-algorithms','medium','concept','Which comparison between batch, mini-batch and stochastic gradient descent is correct?',
    ['Batch uses all training examples per update; mini-batch uses a subset; stochastic uses one example','Batch uses one example; mini-batch uses all examples; stochastic uses a subset','All three necessarily compute identical gradients on each update','Stochastic gradient descent never uses training data'],0,
    'The names describe how many training examples contribute to one gradient estimate. The choice affects computation, noise and update frequency.',
    'Compare the number of examples processed for one parameter update.',
    ['This reverses the standard definitions.','The variants can produce different gradient estimates and trajectories.','Stochastic gradient descent updates using an individual training example.'])

# ----------------------------- PRACTICAL BANK -----------------------------
add('practical','vectors','basic','numerical','Let a=(3,4). What is its Euclidean norm?',
    ['5','7','12','25'],0,
    '||a||₂=√(3²+4²)=√25=5. The norm is the non-negative length of the vector.',
    'Square the components, add them and take the square root.',
    ['7 is the sum of the components, not the Euclidean norm.','12 is not obtained by the Euclidean norm formula.','25 is the squared norm, before taking the square root.'])
add('practical','vectors','medium','numerical','For a=(2,−1,3) and b=(1,4,2), calculate a·b.',
    ['4','8','−4','9'],0,
    'a·b=2(1)+(−1)(4)+3(2)=2−4+6=4.',
    'Multiply corresponding coordinates and sum the three products.',
    ['8 omits the negative middle product.','−4 does not follow from the signed sum.','9 is the sum of selected components rather than all pairwise products.'])
add('practical','vectors','medium','numerical','For a=(4,2) and b=(2,0), calculate proj_b(a).',
    ['(4,0)','(2,0)','(0,2)','(4,2)'],0,
    'proj_b(a)=((a·b)/(b·b))b=(8/4)(2,0)=(4,0). The projection lies along b.',
    'Compute the scalar coefficient first, then multiply b by it.',
    ['(2,0) is the vector b itself, not the projection of a.','This is perpendicular to b, not the component along b.','This returns the original vector instead of its component along b.'])
add('practical','vectors','medium','numerical','What is the cosine similarity between a=(1,0) and b=(0,1)?',
    ['0','1','−1','Undefined'],0,
    'The dot product is zero and both norms are one, so cosine similarity is 0. The vectors are perpendicular.',
    'Use cosine similarity = dot product divided by the product of norms.',
    ['A value of 1 would mean the vectors point in the same direction.','A value of −1 would mean they point in opposite directions.','Both vectors are non-zero, so the similarity is defined.'])
add('practical','vector-spaces','hard','numerical','Do the vectors v₁=(1,2) and v₂=(2,4) form a linearly independent set in ℝ²?',
    ['No; v₂=2v₁, so the set is dependent','Yes; both vectors are non-zero','Yes; two vectors always form a basis of ℝ²','No; because every pair of vectors in ℝ² is dependent'],0,
    'The second vector is exactly twice the first, so one vector is redundant and a non-trivial zero combination exists.',
    'Check whether one vector is a scalar multiple of the other.',
    ['Non-zero vectors can still be scalar multiples and dependent.','Two independent vectors form a basis, but not every pair is independent.','Some pairs, such as (1,0) and (0,1), are independent.'])
add('practical','linear-maps','medium','numerical','A 4×3 matrix has rank 2. What is the nullity of the associated map from ℝ³?',
    ['1','2','3','5'],0,
    'Rank–nullity gives 3=rank+nullity=2+nullity, so nullity is 1.',
    'Use the dimension of the input space, not the number of rows.',
    ['Two is the rank, not the nullity.','Three is the input dimension before subtracting rank.','Five is not compatible with rank–nullity for a 3-dimensional domain.'])
add('practical','matrices','medium','numerical','What is the rank of A=[[1,2,3],[2,4,6]]?',
    ['1','2','3','0'],0,
    'The second row is twice the first, so only one row is linearly independent and rank(A)=1.',
    'Check whether one row is a scalar multiple of the other.',
    ['Two rows do not imply rank two when one is redundant.','A 2×3 matrix cannot have rank three because it has only two rows.','The matrix contains nonzero rows, so its rank is not zero.'])
add('practical','matrices','medium','numerical','Let A=[[1,2],[3,4]] and B=[[0,5],[6,1]]. What is the (1,1) entry of AB using 1-based indexing?',
    ['12','6','18','1'],0,
    'The (1,1) entry is the first row of A dotted with the first column of B: 1·0+2·6=12.',
    'Use row 1 of A and column 1 of B.',
    ['6 is only the second product before the row–column sum.','18 comes from mixing a different row or column.','1 is the first entry of A, not the product entry.'])
add('practical','matrices','medium','numerical','For A=[[2,0],[0,3]], what is det(A)?',
    ['6','5','0','−6'],0,
    'For a 2×2 matrix [[a,b],[c,d]], det=ad−bc. Here 2·3−0=6.',
    'For a diagonal 2×2 matrix, multiply its diagonal entries.',
    ['5 is the trace, not the determinant.','A diagonal matrix with non-zero diagonal entries has non-zero determinant.','The product of positive diagonal entries is positive.'])
add('practical','matrices','medium','numerical','For A=[[1,2],[3,4]], what is Aᵀ?',
    ['[[1,3],[2,4]]','[[1,2],[3,4]]','[[4,2],[3,1]]','[[3,1],[4,2]]'],0,
    'Transpose swaps rows and columns: the first row (1,2) becomes the first column, and the second row (3,4) becomes the second column.',
    'Exchange the row and column indices.',
    ['This is A unchanged, not its transpose.','This is a 180-degree rotation of entries, not a transpose.','This rearrangement does not swap rows and columns correctly.'])
add('practical','matrix-properties','medium','numerical','For M=[[2,1],[1,2]], what is tr(M)?',
    ['4','3','5','2'],0,
    'The trace is the sum of diagonal entries: 2+2=4. Off-diagonal entries are ignored.',
    'Add only the main diagonal.',
    ['3 is a row sum, not the trace.','5 adds all entries.','2 is one diagonal entry, not their sum.'])
add('practical','eigen-pca-svd','medium','numerical','For A=diag(5,2), what is the eigenvalue associated with eigenvector (1,0)?',
    ['5','2','0','7'],0,
    'A(1,0)=(5,0)=5(1,0), so the eigenvalue is 5.',
    'Multiply the matrix by the proposed eigenvector.',
    ['2 is the eigenvalue for direction (0,1).','The transformed vector is not zero.','7 is the sum of diagonal entries, not this eigenvalue.'])
add('practical','eigen-pca-svd','hard','numerical','The eigenvalues of a covariance matrix are 9, 4 and 1. What proportion of total variance is explained by the first principal component?',
    ['9/14 ≈ 64.3%','9/10 = 90%','4/14 ≈ 28.6%','1/14 ≈ 7.1%'],0,
    'Total variance is the sum of eigenvalues: 9+4+1=14. The first component explains 9/14≈0.6429, or 64.3%.',
    'Divide the largest eigenvalue by the sum of all eigenvalues.',
    ['9/10 omits the eigenvalue 4 from total variance.','4/14 is the second component’s share.','1/14 is the third component’s share.'])
add('practical','derivatives','basic','numerical','Differentiate f(x)=x³−4x+7.',
    ['3x²−4','x²−4','3x²+7','x³−4'],0,
    'By the power rule, d(x³)/dx=3x², d(−4x)/dx=−4 and the constant differentiates to zero.',
    'Apply the power rule term by term; constants vanish.',
    ['The power rule reduces the exponent by one and multiplies by the old exponent.','The constant 7 differentiates to zero, not 7.','The expression is missing the derivative of the cubic term.'])
add('practical','derivatives','medium','numerical','For f(x)=(2x+3)⁴, what is f′(x)?',
    ['8(2x+3)³','4(2x+3)³','2(2x+3)⁴','4(2x+3)⁵'],0,
    'By the chain rule, f′=4(2x+3)³·2=8(2x+3)³.',
    'Differentiate the outer fourth power, then multiply by the derivative of 2x+3.',
    ['This omits the inner derivative factor of 2.','This differentiates only the outside function and misses the chain factor.','This leaves the power unchanged and multiplies by 2 incorrectly.'])
add('practical','derivatives','medium','numerical','If f(x)=x² sin(x), what is f′(x)?',
    ['2x sin(x)+x² cos(x)','2x cos(x)+x² sin(x)','x² cos(x)','2x sin(x)'],0,
    'The product rule gives (x²)′sin x+x²(sin x)′=2x sin x+x² cos x.',
    'Treat x² and sin x as the two factors in the product rule.',
    ['This incorrectly swaps the derivative of sine and the original factor.','This omits the derivative of x².','This omits the derivative of the sine factor.'])
add('practical','multivariable','medium','numerical','For f(x,y)=x²+3xy+2y², calculate ∂f/∂x.',
    ['2x+3y','2x+3x+4y','x²+3y+2y²','2x+3xy'],0,
    'Treat y as constant: ∂(x²)/∂x=2x, ∂(3xy)/∂x=3y and ∂(2y²)/∂x=0.',
    'Differentiate only terms that depend on x.',
    ['This differentiates the last term with respect to y and mishandles 3xy.','This leaves an x² term unchanged and is not a partial derivative.','The derivative of 3xy with respect to x is 3y, not 3xy.'])
add('practical','multivariable','hard','numerical','For f(x,y)=x²+xy, what is ∇f at (1,2) using components (∂f/∂x, ∂f/∂y)?',
    ['(4,1)','(2,1)','(4,2)','(3,1)'],0,
    '∂f/∂x=2x+y and ∂f/∂y=x. At (1,2), the gradient is (4,1).',
    'Differentiate with respect to each variable separately, then substitute the point.',
    ['(2,1) omits the y contribution in the x partial.','(4,2) uses the coordinate y for the second partial instead of x.','(3,1) adds x and y incorrectly in the first partial.'])
add('practical','multivariable','hard','numerical','At a point, ∇f=(3,4). What is the directional derivative in the unit direction u=(0.6,0.8)?',
    ['5','3.2','7','0'],0,
    'Dᵤf=∇f·u=3(0.6)+4(0.8)=1.8+3.2=5.',
    'Take the dot product of the gradient with the given unit direction.',
    ['3.2 includes only the second component’s contribution.','7 is the sum of gradient components, not the directional derivative.','The vectors are aligned, not perpendicular.'])
add('practical','gradients-autodiff','hard','numerical','Let L(x,y)=x²y+3y. What is ∂L/∂y?',
    ['x²+3','2xy+3','x²y','2x+y'],0,
    'Differentiate with respect to y while treating x as constant: x²y gives x² and 3y gives 3.',
    'Treat x² as a constant multiplier when differentiating with respect to y.',
    ['2xy+3 is the derivative with respect to x, not y.','This repeats the original product term without differentiating.','This expression is not obtained from the partial derivative.'])
add('practical','vector-matrix-calculus','hard','numerical','For f(x,y)=(x+y, xy), what is the Jacobian under the output-by-input convention?',
    ['[[1,1],[y,x]]','[[1,y],[1,x]]','[[x,y],[1,1]]','[[1,1],[x,y]]'],0,
    'The first output x+y has partials (1,1). The second output xy has partials (y,x). Place outputs in rows and inputs in columns.',
    'Differentiate each output component with respect to x and y.',
    ['This places some derivatives in the wrong input columns.','This is not the required row-by-output arrangement.','This uses function values where partial derivatives are needed.'])
add('practical','optimization','medium','numerical','For f(x)=x² and learning rate η=0.1, one gradient-descent step from x₀=3 gives what x₁?',
    ['2.4','3.6','2.9','0.3'],0,
    'f′(x)=2x, so ∇f(3)=6. Update x₁=3−0.1(6)=2.4.',
    'Compute the derivative at the current point before applying the update.',
    ['3.6 moves in the positive-gradient direction.','2.9 subtracts 0.1 rather than 0.1 times the gradient.','0.3 is the learning-rate times the input, not the updated parameter.'])
add('practical','optimization','hard','numerical','Minimise f(x,y)=x²+y² subject to x+y=2. By symmetry, which point is the constrained minimiser?',
    ['(1,1)','(0,2)','(2,0)','(−1,3)'],0,
    'The constraint line is symmetric in x and y and the squared distance to the origin is minimised at the point on x+y=2 closest to the origin: (1,1). It gives objective 2, less than the alternatives.',
    'The nearest point on the line to the origin lies along its normal direction (1,1).',
    ['(0,2) gives objective 4, which is larger than 2.','(2,0) also gives objective 4.','(−1,3) gives objective 10 and is farther from the origin.'])
add('practical','optimization-algorithms','medium','scenario','A mini-batch contains 32 examples. With 1,024 training examples and no dropped remainder, how many updates are needed for one epoch if every mini-batch produces one update?',
    ['32','16','1,024','64'],0,
    '1,024 ÷ 32 = 32 mini-batches, hence 32 updates in one epoch.',
    'Divide the dataset size by the mini-batch size.',
    ['16 would correspond to batches of 64.','An update is not performed for every individual example in mini-batch training.','64 would correspond to batches of 16.'])
add('practical','optimization-algorithms','hard','scenario','Training loss oscillates and often increases after each update. Which first adjustment is most directly motivated by the gradient-descent update rule?',
    ['Reduce the learning rate','Increase the learning rate substantially','Remove the gradient and update randomly','Replace the objective with its trace'],0,
    'A learning rate that is too large can overshoot minima and cause oscillation or divergence. Reducing it is a direct first diagnostic adjustment, alongside checking gradient scale and implementation.',
    'Consider the size of each step relative to the local curvature.',
    ['A larger step can worsen overshooting.','Random updates do not implement gradient descent.','Trace is a matrix quantity and is not a generic replacement objective.'])
add('practical','search','medium','scenario','A maze has equal cost for every move, and the objective is the path with the fewest moves. Which method is a natural choice?',
    ['Breadth-first search','Depth-first search with arbitrary branch order','Uniform random search','Backward chaining over predicate rules'],0,
    'With equal step costs, BFS expands by depth and finds a shallowest goal, hence a minimum-number-of-moves path.',
    'Equal move costs mean the fewest edges is also the least-cost path.',
    ['DFS does not guarantee the shallowest solution.','Random search offers no shortest-path guarantee.','Backward chaining is a logic reasoning strategy rather than the natural maze-path algorithm.'])
add('practical','agents-csp','hard','scenario','A timetable assigns each exam a time slot. Two exams taken by the same student cannot overlap. In CSP terms, the “cannot overlap” rule is:',
    ['A constraint relating the time-slot variables of those exams','A domain value for every student','The objective function that maximises the number of exams','A transition model describing a search tree'],0,
    'The rule restricts which pairs of variable assignments are allowed, so it is a constraint. Each exam is a variable and its possible slots form its domain.',
    'Identify which statement rules out combinations of assignments.',
    ['The domain is the list of allowed time slots, not the compatibility rule.','Maximising a count is a different optimisation objective.','A transition model describes state changes, not the CSP rule itself.'])
add('practical','logic','medium','numerical','If P is true and Q is false, what is the truth value of P → Q?',
    ['False','True','Both true and false','Undefined'],0,
    'Material implication is false only when the antecedent is true and the consequent is false.',
    'Check the one counterexample row in the implication truth table.',
    ['This is the exact false row of implication.','It would be true if P were false or Q were true.','Classical propositional logic assigns a definite truth value.'])
add('practical','reasoning-planning','hard','numerical','Resolve (P ∨ Q) with (¬P ∨ R) on the complementary pair P and ¬P. What is the result?',
    ['Q ∨ R','P ∧ R','¬Q ∨ ¬R','P ∨ ¬P'],0,
    'Remove P and ¬P, then combine the remaining literals Q and R to produce Q ∨ R.',
    'Resolution removes the chosen complementary literals.',
    ['The resolvent is a disjunction of remaining literals, not a conjunction.','Negating the remaining literals is not part of the rule.','P ∨ ¬P is a tautology and not the computed resolvent.'])

# ---------------------------- EXTENSION BANK ------------------------------
# These items are explicitly supplementary, not syllabus claims.
add('extension','big-data','medium','supplement','Which measure is resistant to a small number of extremely large outliers?',
    ['Median','Arithmetic mean','Maximum','Range'],0,
    'The median depends on the middle order statistic and is less affected by extreme values than the mean, maximum or range.',
    'Think of a measure based on the ordered position rather than the magnitude of every value.',
    ['The mean can be pulled strongly by extreme values.','The maximum is defined by the largest observation and is directly sensitive to an outlier.','The range depends directly on the minimum and maximum.'])
add('extension','big-data','medium','supplement','For the data [2, 4, 4, 6], what is the population variance?',
    ['2','4','1','8'],0,
    'The mean is 4. Squared deviations are 4, 0, 0, 4, whose population average is 8/4=2.',
    'Find the mean, square each deviation and divide by N for population variance.',
    ['4 is the population standard deviation squared incorrectly or an unnormalised quantity.','1 is not the mean squared deviation.','8 is the sum of squared deviations before dividing by N.'])
add('extension','big-data','hard','supplement','A classifier detects a rare failure where missing a true failure is much more costly than a false alarm. Which metric is especially important to inspect alongside precision?',
    ['Recall','R-squared','Silhouette score','Matrix trace'],0,
    'Recall measures the proportion of actual positive failures detected. When false negatives are costly, recall is particularly important, though the decision threshold and precision trade-off also matter.',
    'Focus on the cost of failing to detect a real positive case.',
    ['R-squared is typically a regression fit measure.','Silhouette score evaluates clustering separation.','Trace is a matrix property, not a classification metric.'])
add('extension','ml-learning','medium','supplement','What is overfitting?',
    ['A model fits training data patterns, including noise, but generalises poorly to unseen data','A model performs poorly on both training and test data because it is too simple','A model has exactly equal training and test error','A model is evaluated without any data'],0,
    'Overfitting occurs when a model captures idiosyncrasies or noise in training data and consequently has a generalisation gap.',
    'Compare performance on training examples with performance on unseen examples.',
    ['This describes underfitting more closely.','Equal errors are not the defining feature and can occur at many performance levels.','Evaluation without data is not overfitting.'])
add('extension','ml-learning','medium','supplement','What is the main purpose of splitting labelled data into training, validation and test sets?',
    ['Train parameters, select/tune models, and estimate final generalisation respectively','Use all three sets to update model weights equally','Ensure every split has different feature definitions','Remove the need for an appropriate evaluation metric'],0,
    'The training set fits parameters; validation supports model selection and tuning; the test set is reserved for a final, less biased evaluation.',
    'Each split should have a distinct role in the modelling workflow.',
    ['Using the test set for repeated weight updates leaks evaluation information.','All splits should represent the same feature schema.','A sound metric is still needed to evaluate the target task.'])
add('extension','vectors','medium','supplement','Why are feature standardisation and scaling often considered before distance-based machine learning?',
    ['Features with large numeric scales can dominate distance calculations','Scaling always increases the number of features','Scaling guarantees that classes become linearly separable','Scaling converts every feature into a categorical label'],0,
    'Distance-based methods can be dominated by features measured on large numeric scales. Scaling can make contributions more comparable when that is appropriate for the task.',
    'Think about how a large unit range affects Euclidean distance.',
    ['Scaling does not inherently add features.','No scaling method guarantees linear separability.','Standardisation typically preserves numeric values rather than turning them into categories.'])
add('extension','eigen-pca-svd','hard','supplement','Why should PCA usually be fitted on the training split and then applied to validation/test data?',
    ['To avoid information leakage from evaluation data into the learned projection','Because PCA cannot transform data it has not seen','Because test data must have different columns','To force every principal component to explain equal variance'],0,
    'Fitting preprocessing on all data lets information from held-out observations influence the representation. Fit the PCA transform on training data, then apply that fitted transform to held-out sets.',
    'Ask whether the held-out data influence a transformation that is meant to be learned from training only.',
    ['PCA can transform unseen samples using the fitted loadings.','Feature columns must be aligned, not different.','Principal components generally explain different amounts of variance.'])
add('extension','ml-learning','hard','supplement','What does regularisation do in many machine-learning objectives?',
    ['Adds a penalty or constraint that discourages overly complex parameter values','Guarantees zero training error','Replaces the need for training data','Makes every parameter increase during optimisation'],0,
    'Regularisation adds a complexity penalty or constraint, such as an L1 or L2 term, to encourage solutions that may generalise better.',
    'Look for an extra term in the objective that discourages complexity.',
    ['Regularisation may increase training error slightly while improving generalisation.','It does not eliminate the need for data.','The penalty does not force parameters to increase.'])
add('extension','big-data','medium','supplement','Bayes’ theorem is useful because it allows one to:',
    ['Update a probability for a hypothesis using observed evidence','Calculate a matrix inverse from its trace alone','Guarantee that a classifier is unbiased','Convert an unsupervised task into a deterministic search tree'],0,
    'Bayes’ theorem relates posterior, likelihood and prior: P(H|E)=P(E|H)P(H)/P(E), for P(E)>0.',
    'Recall the relationship between prior belief, evidence and posterior belief.',
    ['Trace alone is insufficient to determine a matrix inverse.','Bayesian updating does not guarantee fairness or eliminate bias.','The theorem is probabilistic inference, not a conversion to search.'])
add('extension','big-data','medium','supplement','A 95% confidence interval procedure is interpreted correctly as:',
    ['Across repeated samples, about 95% of intervals constructed by the procedure would contain the fixed true parameter','There is a 95% probability that this already-computed interval contains the fixed parameter','95% of observations lie inside every confidence interval','The sample mean is correct 95% of the time'],0,
    'In the frequentist interpretation, the confidence level describes the long-run coverage rate of the procedure under its assumptions, not a probability assigned to the fixed parameter after observing one interval.',
    'Think about repeated sampling and the behaviour of the interval-building procedure.',
    ['The parameter is fixed in the frequentist framework; the interval is random before sampling.','A confidence interval for a parameter is not an interval expected to contain 95% of individual observations.','Coverage does not mean the sample mean is exactly correct in 95% of repetitions.'])
add('extension','optimization','hard','supplement','What is the main purpose of a learning-rate schedule in gradient-based training?',
    ['To change the step size over training to balance progress and stability','To change the target labels after each epoch','To guarantee convergence to the global minimum for every objective','To eliminate the need to calculate gradients'],0,
    'A schedule varies the learning rate over time, for example using larger early steps and smaller later steps, to balance speed and stability. It does not guarantee global optimality for arbitrary non-convex objectives.',
    'The learning rate is the scale applied to each gradient update.',
    ['Labels define the learning target and are not a learning-rate schedule.','Non-convex optimisation has no general global convergence guarantee from a schedule alone.','Gradient-based schedules still use gradients.'])
add('extension','ml-learning','hard','supplement','What is data leakage in a machine-learning workflow?',
    ['Information unavailable at prediction time improperly influences training or evaluation','A dataset is stored on a disk drive instead of memory','The training set contains multiple feature columns','A model has fewer parameters than observations'],0,
    'Leakage occurs when information from validation/test data, future outcomes or otherwise unavailable variables contaminates model development, leading to over-optimistic evaluation.',
    'Ask whether the model has access to information it would not legitimately have at prediction time.',
    ['Storage location is not data leakage.','Multiple feature columns are normal.','The parameter-to-observation ratio is not the definition of leakage.'])
add('extension','derivatives','medium','supplement','What does the Hessian of a twice-differentiable scalar function contain?',
    ['All second-order partial derivatives','All first-order partial derivatives only','The sorted eigenvectors of the input matrix','The function values at every point in the domain'],0,
    'The Hessian is the square matrix whose (i,j) entry is the second partial derivative ∂²f/(∂xᵢ∂xⱼ).',
    'It is the second-derivative analogue of the gradient.',
    ['The first derivatives make up the gradient.','Eigenvectors may be used to analyse the Hessian but are not its entries.','A Hessian is local derivative information, not a full table of function values.'])
add('extension','eigen-pca-svd','hard','supplement','For a covariance matrix, why are negative eigenvalues a warning sign in exact arithmetic?',
    ['A covariance matrix is positive semidefinite, so its eigenvalues should be non-negative','A covariance matrix must have all eigenvalues strictly negative','Eigenvalues of every matrix are always positive','A negative eigenvalue proves that the data have no variance'],0,
    'For any vector x, xᵀΣx is the variance of a linear combination and cannot be negative; therefore an exact covariance matrix is positive semidefinite. Small negative numerical values may arise from floating-point error.',
    'Connect covariance to variance of a projected variable.',
    ['Strict positivity is not guaranteed; zero eigenvalues are possible.','General matrices can have negative eigenvalues, but a covariance matrix cannot in exact arithmetic.','A negative eigenvalue is not proof that the data have no variance; it signals invalidity or numerical issues.'])
add('extension','optimization-algorithms','hard','supplement','Why can mini-batch training be faster in practice than pure stochastic updates on modern accelerators?',
    ['Vectorised operations on a batch can use hardware efficiently while averaging some gradient noise','A batch makes each gradient mathematically exact for every possible dataset','Mini-batch updates never require memory for examples','A mini-batch automatically removes all local minima'],0,
    'Batched matrix operations can exploit parallel hardware and reduce per-example overhead. The estimated gradient remains noisy relative to the full-batch gradient.',
    'Consider hardware utilisation and the number of samples processed together.',
    ['Only a full-data gradient is exact for the full empirical objective.','Mini-batches require storing or streaming data for the batch.','Batch size does not remove local minima from the objective landscape.'])
add('extension','big-data','medium','supplement','In a binary classifier, precision is defined as:',
    ['TP/(TP+FP)','TP/(TP+FN)','TN/(TN+FP)','(TP+TN)/(TP+TN+FP+FN)'],0,
    'Precision is the fraction of predicted positives that are true positives. Recall is TP/(TP+FN), specificity is TN/(TN+FP), and accuracy is the fraction of all predictions that are correct.',
    'Precision asks: of the cases predicted positive, how many were actually positive?',
    ['This is recall.','This is specificity.','This is accuracy.'])
add('extension','big-data','hard','supplement','A dataset is highly imbalanced, with 99% negative cases. Why can accuracy be misleading?',
    ['A model predicting the majority class every time can score 99% accuracy while detecting no positives','Accuracy is undefined when class frequencies differ','Accuracy gives extra weight to the minority class','Accuracy is always lower than precision'],0,
    'A majority-class-only classifier would achieve 99% accuracy in this example but have zero recall for the minority positive class. Use a metric set aligned to the costs and class distribution.',
    'Consider the trivial strategy of always predicting the majority class.',
    ['Accuracy remains defined with class imbalance.','Accuracy does not intrinsically up-weight the minority class.','There is no universal ordering between accuracy and precision.'])
add('extension','ml-learning','medium','supplement','What does cross-validation primarily help estimate during model development?',
    ['How model performance varies across different training/validation splits','The exact global optimum of the loss function','The number of hidden layers required in every network','Whether the labels are legally valid'],0,
    'Cross-validation repeatedly trains and validates across folds, providing a more robust estimate of performance and model-selection stability than a single split in many settings.',
    'Think about repeated partitions and validation scores.',
    ['Cross-validation does not solve global optimisation.','It can support model selection but does not prescribe a universal architecture.','Label legality and governance need separate review.'])
add('extension','optimization','hard','supplement','What is the vanishing-gradient problem in a deep network?',
    ['Gradients become extremely small as they propagate backward, making early layers learn very slowly','Gradients become infinite after every update','The model has no loss function','Every activation becomes exactly zero for all inputs'],0,
    'Repeated multiplication by derivatives with magnitude below one can shrink gradients as they propagate backward through many layers, reducing learning signals for earlier layers.',
    'Consider repeated products of small local derivatives in the chain rule.',
    ['Exploding gradients are associated with very large, not small, values.','A loss function is still present.','Vanishing gradients do not require every activation to be exactly zero.'])


# Additional items to complete this curated release's coverage.
add('core','linear-maps','medium','concept','A transformation is T(x)=Ax+b with b non-zero. How should it generally be classified?',
    ['An affine transformation, not a linear map','A linear map because A is a matrix','A projection because b is constant','An orthogonal transformation by definition'],0,
    'A nonzero translation term means T(0)=b rather than zero, so the transformation is affine and generally not linear.',
    'Test what happens to the zero vector.',
    ['The presence of a matrix A does not remove the nonzero translation term.','A constant translation is not the same as a projection.','Orthogonality requires a specific inner-product-preserving linear transformation.'])

add('practical','matrices','hard','numerical','For A=[[1,2],[3,4]], calculate det(A).',
    ['−2','2','10','−10'],0,
    'det(A)=1·4−2·3=4−6=−2. The negative sign indicates orientation reversal for this two-dimensional linear map.',
    'For a 2×2 matrix use ad−bc.',
    ['2 has the wrong sign because the cross-product term is larger.','10 is the sum of all entries.','−10 is not the determinant calculation.'])
add('practical','matrices','hard','numerical','For A=[[2,0],[0,4]], what is A⁻¹?',
    ['[[1/2,0],[0,1/4]]','[[2,0],[0,4]]','[[4,0],[0,2]]','[[−2,0],[0,−4]]'],0,
    'The inverse of an invertible diagonal matrix is diagonal with reciprocal diagonal entries.',
    'Find the matrix that multiplies A to give the identity.',
    ['This is A itself, and A·A is not the identity.','Swapping diagonal entries does not create the inverse.','Negating entries is not the inverse operation.'])
add('practical','matrix-properties','medium','numerical','A matrix has eigenvalues 3, 3 and 0. What is its rank if it is diagonalizable and is a 3×3 matrix?',
    ['2','1','3','0'],0,
    'For a diagonalizable matrix, the algebraic multiplicity pattern gives two nonzero eigen-directions and one zero eigen-direction, so the rank is 2.',
    'For a diagonalizable matrix, rank equals the number of nonzero eigenvalues counted with multiplicity.',
    ['One is the nullity, not the rank.','The zero eigenvalue does not make the matrix full rank.','Two nonzero eigenvalues mean the matrix is not rank zero.'])
add('practical','eigen-pca-svd','hard','numerical','For A=[[2,0],[0,5]], which polynomial equation gives its eigenvalues?',
    ['(2−λ)(5−λ)=0','(2+λ)(5+λ)=0','λ²+7=0','(2−λ)+(5−λ)=0'],0,
    'The characteristic equation is det(A−λI)=0, which for this diagonal matrix is (2−λ)(5−λ)=0.',
    'Subtract λ from each diagonal entry and take the determinant.',
    ['The sign in A−λI is not plus.','The determinant gives a quadratic with real roots 2 and 5.','The determinant of a diagonal matrix is the product of its diagonal entries, not their sum.'])
add('practical','derivatives','hard','numerical','For f(x)=(x²+1)/x with x≠0, which simplified derivative is correct?',
    ['1−1/x²','1+1/x²','2x/x','x²−1'],0,
    'Rewrite f(x)=x+x⁻¹. Then f′(x)=1−x⁻²=1−1/x².',
    'Simplify the quotient before differentiating.',
    ['The derivative of x⁻¹ is negative x⁻².','The derivative of x⁻¹ is not positive x⁻².','2x/x simplifies to 2 and is not the derivative.'])
add('practical','multivariable','hard','numerical','For f(x,y)=x²+y², calculate the directional derivative at (1,1) in direction u=(1/√2,1/√2).',
    ['2√2','2','√2','0'],0,
    'The gradient at (1,1) is (2,2). Its dot product with the unit direction is 2/√2+2/√2=2√2.',
    'Evaluate the gradient at the point and dot it with the unit direction.',
    ['2 omits the combined contribution from both coordinates.','√2 is half the correct dot product.','The gradient and direction point the same way, so the derivative is not zero.'])
add('practical','gradients-autodiff','hard','numerical','For f(x,y)=x²+4y², what is the Hessian matrix?',
    ['[[2,0],[0,8]]','[[2,0],[0,4]]','[[x,0],[0,y]]','[[0,0],[0,0]]'],0,
    'The first partials are 2x and 8y. Differentiating again gives fxx=2, fxy=0, fyx=0 and fyy=8.',
    'Differentiate twice and arrange second partial derivatives by variable.',
    ['The y² term differentiates twice to 8, not 4.','A Hessian contains second derivatives, not the input coordinates.','The second derivatives are not all zero for this quadratic.'])
add('practical','optimization','hard','numerical','For f(x)=x²−6x+10, at what x-value is the unconstrained minimum attained?',
    ['3','−3','6','0'],0,
    'Set f′(x)=2x−6=0, giving x=3. Since f″(x)=2>0, this stationary point is a minimum.',
    'Set the first derivative to zero, then check the second derivative.',
    ['The negative root solves 2x+6=0, not the actual derivative equation.','6 is the coefficient of x, not the minimiser.','The derivative at zero is −6, so zero is not stationary.'])
add('practical','optimization-algorithms','medium','scenario','A convex differentiable objective has a feasible local minimiser. What can be concluded about that minimiser?',
    ['It is also a global minimiser','It must be a saddle point','It must be the only feasible point','Its gradient must be non-zero'],0,
    'For a convex objective over a convex feasible set, every local minimum is global. The minimum need not be unique unless stronger assumptions hold.',
    'Recall the local-to-global property of convex optimisation.',
    ['Convexity rules out a nonglobal local minimum.','A local minimiser is not a saddle point by definition.','The feasible set can contain many points.','At an unconstrained differentiable interior minimum the gradient is zero; constrained conditions require more care.'])
add('practical','agents-csp','hard','scenario','In a CSP, a variable has domain {1,2,3}. After assigning a neighbouring variable, a constraint rules out value 2. What is the remaining domain?',
    ['{1,3}','{2}','{1,2,3}','The empty set'],0,
    'Constraint propagation removes inconsistent values from the domain, leaving 1 and 3.',
    'Remove only the value explicitly ruled out by the constraint.',
    ['The ruled-out value cannot remain by itself.','The domain is not unchanged because value 2 is inconsistent.','There are still two remaining legal values, so the domain is not empty.'])
add('practical','big-data','medium','scenario','A data file contains rows with fixed columns (timestamp, sensor_id, temperature). How is it classified in the syllabus distinction?',
    ['Structured data','Unstructured data','A rule base','A state-space transition model'],0,
    'The data have a regular schema with named fields and consistent records, so they are structured data.',
    'Check whether the values follow a predefined tabular schema.',
    ['Free-form text, images and audio are common examples of unstructured data.','A rule base stores logic rules, not sensor observations in tabular records.','A transition model describes state changes in a search problem.'])
add('extension','big-data','medium','supplement','A value is 80, the sample mean is 50 and the standard deviation is 10. What is its z-score?',
    ['3','30','0.3','8'],0,
    'z=(x−μ)/σ=(80−50)/10=3. The value is three standard deviations above the mean.',
    'Subtract the mean from the observation and divide by the standard deviation.',
    ['30 is the difference from the mean before standardising.','0.3 divides by 100 rather than 10.','8 is the observation divided by the standard deviation without centring.'])


# Expanded syllabus coverage for session topics that deserve explicit assessment.
add('core','ai-foundations','medium','concept','Which sequence best represents a common high-level flow in an AI application?',
    ['Input/perception, representation or model processing, decision, and output/action','Output/action, then input, with no intermediate processing','Database storage only, followed by a fixed report','Training labels, then a matrix inverse, regardless of the task'],0,
    'Many AI systems receive inputs, extract or represent relevant information, reason or predict, and then produce an output or action. The exact architecture depends on the application.',
    'Trace information from the environment through processing to a system response.',
    ['A useful system ordinarily processes input before producing an action.','Storage may be one component but is not the entire AI flow.','The workflow is not restricted to labels or matrix inversion.'])
add('core','ai-history','medium','concept','Which statement best describes the broad shift in AI methods across its history?',
    ['AI has included symbolic reasoning and expert systems as well as statistical learning and modern neural approaches','AI history consists only of the recent introduction of chatbots','Symbolic reasoning was never used in AI','Every modern AI system is based exclusively on a Turing Machine implementation'],0,
    'AI has evolved through several approaches, including symbolic methods, knowledge-based expert systems, statistical learning and neural methods. These approaches are not mutually exclusive.',
    'Think of several generations and families of AI techniques rather than a single invention.',
    ['AI research predates recent chatbots by decades.','Symbolic reasoning and expert systems are important historical AI approaches.','A Turing Machine is a theoretical model of computation, not the exclusive implementation of modern AI.'])
add('core','ai-systems','medium','concept','What is a useful distinction between a rule-based system and a machine-learning model?',
    ['A rule-based system applies explicitly encoded rules, while a learned model derives patterns from training data','A rule-based system always uses more data than a learned model','A learned model cannot produce predictions','A rule-based system and a learned model are identical by definition'],0,
    'Rule-based systems rely on explicitly represented conditions and rules. Machine-learning models fit parameters or structures from data; hybrid systems may combine both.',
    'Ask where the decision logic comes from: written rules or patterns learned from examples.',
    ['Rule-based systems can operate with limited data and do not inherently require a larger dataset.','Prediction is a core use of learned models.','The two approaches have distinct knowledge and learning mechanisms.'])
add('core','ml-learning','medium','concept','A robot improves its navigation policy by trying actions and receiving feedback from the environment. Which learning idea is most closely related?',
    ['Learning through interaction and feedback','Unsupervised clustering of fixed customer records','Static rule lookup with no feedback','Dimensionality reduction of a covariance matrix'],0,
    'Learning through interaction uses consequences or feedback from actions to improve behaviour. This is conceptually related to reinforcement-learning settings, though the syllabus names the broader interaction idea.',
    'The system changes its behaviour based on outcomes of its own actions.',
    ['Clustering fixed records does not describe an action–feedback loop.','A static lookup system does not learn from interaction.','Covariance decomposition is a linear-algebra task, not interactive learning.'])
add('core','search','medium','concept','What is the main idea behind parallel search?',
    ['Explore different parts of the search space concurrently using multiple processing resources','Convert every search problem into a matrix multiplication','Guarantee that each worker finds a different optimal solution','Remove the need for a goal test and state representation'],0,
    'Parallel search divides exploration work across processing resources. Practical performance depends on task partitioning, communication, synchronisation and load balance.',
    'Look for multiple branches or subproblems being explored at the same time.',
    ['Matrix multiplication is not the defining operation of parallel search.','Workers may explore overlapping regions, and a single solution may be sought.','A valid problem formulation and goal test are still required.'])
add('core','search','medium','concept','In a search engine, what is the purpose of ranking after candidate documents have been retrieved?',
    ['Order retrieved documents by estimated relevance to the user query','Change the original text of every retrieved document','Guarantee that every relevant document is indexed','Compute the inverse of the query-term matrix'],0,
    'Retrieval finds candidate documents and ranking orders them according to estimated relevance or other ranking signals. Ranking does not guarantee complete indexing or perfect relevance.',
    'Think about what the user sees first on a results page.',
    ['Ranking normally orders results rather than rewriting source documents.','Ranking cannot guarantee that all relevant material was indexed.','Matrix inversion is not the general purpose of search-result ranking.'])
add('core','logic','medium','concept','Which statement best describes logic programming?',
    ['Facts and rules are declared, and queries are answered through logical inference','Every operation must be written as a sequence of machine-level instructions','It is a numerical optimisation method for eigenvectors','It stores only unlabelled image pixels'],0,
    'Logic programming represents relationships declaratively using facts and rules; a query asks whether a goal follows through inference.',
    'The program describes relationships that should hold, then asks a query.',
    ['Logic programming is declarative rather than a list of low-level instructions.','Eigenvector optimisation is unrelated to its defining paradigm.','Image pixels may be data for AI but do not define logic programming.'])
add('core','matrix-properties','medium','concept','Why is low-rank matrix approximation useful in data analysis?',
    ['It can retain dominant structure while reducing storage or computation','It guarantees that every original matrix entry remains exactly unchanged','It increases matrix rank to the maximum possible value','It removes the need to choose an approximation tolerance or rank'],0,
    'A low-rank approximation represents a matrix using fewer independent directions, often retaining dominant patterns while reducing storage, noise or computation. The trade-off is approximation error.',
    'Think about representing a large matrix with fewer degrees of freedom.',
    ['An approximation generally changes some entries or reconstruction values.','Low-rank approximation reduces rank rather than maximising it.','The chosen rank controls the trade-off between compactness and fidelity.'])

# Additional practical problem-solving items.
add('practical','vectors','medium','numerical','For v=(2,−2), what is the unit vector in the direction of v?',
    ['(1/√2, −1/√2)','(2,−2)','(1/2,−1/2)','(−1/√2, 1/√2)'],0,
    'The norm is √(4+4)=2√2. Dividing v by its norm gives (1/√2,−1/√2).',
    'A unit vector is the original vector divided by its Euclidean norm.',
    ['This vector has norm 2√2, not 1.','Dividing by 2 gives a vector of norm √2, not 1.','This points in the opposite direction.'])
add('practical','vector-spaces','hard','numerical','The columns of a 3×3 matrix are linearly independent. What is the dimension of their span?',
    ['3','2','1','0'],0,
    'Three linearly independent vectors in ℝ³ form a basis of ℝ³, so their span has dimension 3.',
    'The dimension of a span equals the number of independent vectors in a basis for that span.',
    ['Two would mean one of the three independent directions is missing.','One would describe three collinear vectors, which are not independent.','Non-zero independent columns do not span only the zero vector.'])
add('practical','matrices','hard','numerical','Let A=[[1,0],[0,2]] and B=[[0,1],[1,0]]. What is AB?',
    ['[[0,1],[2,0]]','[[0,2],[1,0]]','[[1,0],[0,2]]','[[0,1],[1,0]]'],0,
    'Multiply rows of A by columns of B: AB=[[0,1],[2,0]]. The result differs from BA, illustrating non-commutativity.',
    'Compute each entry using row-by-column multiplication, preserving the order A then B.',
    ['This is BA, not AB.','This is A, not the product.','This is B, not the product.'])
add('practical','multivariable','hard','numerical','For f(x,y)=3x²y−y³, what is ∂f/∂x at (2,1)?',
    ['12','11','6','3'],0,
    '∂f/∂x=6xy. At (2,1), the value is 6·2·1=12.',
    'Treat y as constant and differentiate only with respect to x.',
    ['11 incorrectly includes the derivative of the y-only term.','6 omits the x=2 factor.','3 is a coefficient, not the evaluated partial derivative.'])
add('practical','optimization-algorithms','hard','numerical','For f(x)=x², starting at x₀=−2 with η=0.25, what is one gradient-descent update?',
    ['−1','−3','−2.5','0'],0,
    'f′(−2)=−4. The update is x₁=−2−0.25(−4)=−1.',
    'A negative gradient means subtracting it moves x in the positive direction.',
    ['−3 moves opposite to the correct update direction.','−2.5 uses only part of the gradient incorrectly.','One step does not reach the minimum exactly in this case.'])
add('practical','reasoning-planning','hard','scenario','A planner can apply action “open door” only when “door unlocked” is true. After the action, “door open” becomes true. Which pair is correct?',
    ['Precondition: door unlocked; effect: door open','Precondition: door open; effect: door unlocked','Precondition: door unlocked; effect: door remains locked','Precondition: door open; effect: no state change'],0,
    'The unlocked condition must hold before the action, and the action changes the state so that the door is open.',
    'Separate what must already hold from what the action makes true.',
    ['This reverses the precondition and effect.','The effect should represent the change caused by the action.','The action’s stated outcome is not that the door remains locked.'])

# Syllabus-specific matrix phylogeny item: relationship map across matrix classes.
add('core','matrix-phylogeny','hard','concept','What does the “matrix phylogeny” diagram summarise in the matrix-decomposition material?',
    ['Relationships and subset structure among matrix classes, together with properties or operations associated with them','A chronological history of when individual matrix entries were discovered','A method for clustering rows without using matrix properties','A proof that every invertible matrix is diagonalizable over the real numbers'],0,
    'Matrix phylogeny is a functional relationship map: it organises matrix classes such as square, singular, invertible, normal, symmetric, orthogonal and positive definite, and links them to properties or operations such as determinant, inverse, eigen-decomposition and SVD. Invertibility and real diagonalizability are distinct properties.',
    'Think of a map of matrix types and the properties that distinguish or connect them.',
    ['It is not a historical timeline of matrix notation.','Clustering rows is not the chapter’s meaning of matrix phylogeny.','An invertible matrix need not be diagonalizable over the real numbers.'])

# Sanity checks, stable global numbering and output files.
assert len([r for r in rows if r['bank']=='core']) == 69
assert len([r for r in rows if r['bank']=='practical']) == 46
assert len([r for r in rows if r['bank']=='extension']) == 20
ids = [r['id'] for r in rows]
nums = [r['number'] for r in rows]
assert len(ids) == len(set(ids)) and len(nums) == len(set(nums))
for bank, filename in [('core','questions-core.json'),('practical','questions-practical.json'),('extension','questions-extension.json')]:
    bank_data = [r for r in rows if r['bank']==bank]
    (ROOT/'data'/filename).write_text(json.dumps(bank_data, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'Generated {len(rows)} questions: core=69, practical=46, extension=20')
