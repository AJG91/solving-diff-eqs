"""
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patheffects as mpe
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from numpy.typing import ArrayLike

exact_kwargs = dict(ls="solid", lw=1, zorder=1)
numerical_kwargs = dict(dash_capstyle="round", ls=(0, (0.1, 2)), zorder=2, lw=7, 
                        path_effects=[mpe.withStroke(linewidth=4, foreground="k")])

numerical_color = "lightsalmon"
exact_color = "black"

numerical_label = "Numerical"
exact_label = "Exact"

def setup_rc_params(presentation=False, constrained_layout=True, usetex=True, dpi=400):
    if presentation:
        fontsize = 11
    else:
        fontsize = 9
    black = "k"

    mpl.rcdefaults()  # Set to defaults
    x_minor_tick_size = y_minor_tick_size = 2.4
    x_major_tick_size = y_major_tick_size = 3.9

    # mpl.rc("text", usetex=True)
    mpl.rcParams["font.size"] = fontsize
    mpl.rcParams["text.usetex"] = usetex
    # mpl.rcParams["text.latex.preview"] = True
    mpl.rcParams["font.family"] = "serif"

    mpl.rcParams["axes.labelsize"] = fontsize
    mpl.rcParams["axes.edgecolor"] = black
    # mpl.rcParams['axes.xmargin'] = 0
    mpl.rcParams["axes.labelcolor"] = black
    mpl.rcParams["axes.titlesize"] = fontsize

    mpl.rcParams["ytick.direction"] = "in"
    mpl.rcParams["xtick.direction"] = "in"
    mpl.rcParams["xtick.labelsize"] = fontsize
    mpl.rcParams["ytick.labelsize"] = fontsize
    mpl.rcParams["xtick.color"] = black
    mpl.rcParams["ytick.color"] = black
    # Make the ticks thin enough to not be visible at the limits of the plot (over the axes border)
    mpl.rcParams["xtick.major.width"] = mpl.rcParams["axes.linewidth"] * 0.95
    mpl.rcParams["ytick.major.width"] = mpl.rcParams["axes.linewidth"] * 0.95
    # The minor ticks are little too small, make them both bigger.
    mpl.rcParams["xtick.minor.size"] = x_minor_tick_size  # Default 2.0
    mpl.rcParams["ytick.minor.size"] = y_minor_tick_size
    mpl.rcParams["xtick.major.size"] = x_major_tick_size  # Default 3.5
    mpl.rcParams["ytick.major.size"] = y_major_tick_size
    plt.rcParams["xtick.minor.visible"] =  True
    plt.rcParams["ytick.minor.visible"] =  True

    ppi = 72  # points per inch
    mpl.rcParams["figure.titlesize"] = fontsize
    mpl.rcParams["figure.dpi"] = 150  # To show up reasonably in notebooks
    mpl.rcParams["figure.constrained_layout.use"] = constrained_layout
    # 0.02 and 3 points are the defaults:
    # can be changed on a plot-by-plot basis using fig.set_constrained_layout_pads()
    mpl.rcParams["figure.constrained_layout.wspace"] = 0.02
    mpl.rcParams["figure.constrained_layout.hspace"] = 0.0
    mpl.rcParams["figure.constrained_layout.h_pad"] = 0#3.0 / ppi
    mpl.rcParams["figure.constrained_layout.w_pad"] = 0#3.0 / ppi

    mpl.rcParams["text.latex.preamble"] = r"\usepackage{amsfonts}"

    mpl.rcParams["legend.title_fontsize"] = fontsize
    mpl.rcParams["legend.fontsize"] = fontsize
    mpl.rcParams[
        "legend.edgecolor"
    ] = "inherit"  # inherits from axes.edgecolor, to match
    mpl.rcParams["legend.facecolor"] = (
        1,
        1,
        1,
        0.6,
    )  # Set facecolor with its own alpha, so edgecolor is unaffected
    mpl.rcParams["legend.fancybox"] = True
    mpl.rcParams["legend.borderaxespad"] = 0.8
    mpl.rcParams[
        "legend.framealpha"
    ] = None  # Do not set overall alpha (affects edgecolor). Handled by facecolor above
    mpl.rcParams[
        "patch.linewidth"
    ] = 0.8  # This is for legend edgewidth, since it does not have its own option

    mpl.rcParams["hatch.linewidth"] = 0.5
    
    return None

def compute_error(
    A: ArrayLike, 
    B: ArrayLike, 
    error: str
) -> ArrayLike:
    """
    Used to calculate relative or absolute error.

    Parameters
    ----------
    A : array
        Expected values.
    B : array
        Actual values observed.
    error : str
        Used to choose between relative or absolute errors.
        'Rel.' == relative errors
        'Abs.' == absolute errors

    Returns
    -------
    err : array
        Errors
    """
    if error == 'Rel.':
        return 2 * abs(A - B) / (abs(A) + abs(B))
    elif error == 'Abs.':
        return abs(A - B)
    else:
        raise ValueError('Check error input!')

def velocity_vs_time_graph(
    t: ArrayLike, 
    v_exact: ArrayLike, 
    v_num: ArrayLike, 
    error: str
) -> None:
    """
    Used to plot a velocity vs. time using the exact and numerical solution with errors.

    Parameters
    ----------
    t : array
        Time values.
    v_exact : array
        Exact velocity values calculated from the kinematics equations.
    v_num : array
        Numerical velocity values calculated by solving the differential equations.
    error : str
        Used to choose between relative or absolute errors.
        "Rel." == relative errors
        "Abs." == absolute errors

    Returns
    -------
    None
    """
    fig = plt.figure(figsize=(8, 4))

    ax1 = fig.add_subplot(1, 2, 1)
    ax1.plot(t, v_num, c=numerical_color, label=numerical_label, **numerical_kwargs)
    ax1.plot(t, v_exact, c=exact_color, label=exact_label, **exact_kwargs)
    ax1.set_xlabel(r"$t$ [s]")
    ax1.set_ylabel(r"$v(t)$ [m/s]")
    ax1.set_title(r"Velocity vs. time")
    ax1.legend();
    
    ax2 = fig.add_subplot(1, 2, 2)
    ax2.semilogy(t, compute_error(v_exact, v_num.flatten(), error), color="red")
    ax2.set_ylim(1e-20, 1e0)
    ax2.set_xlabel(r"$t$ [s]")
    ax2.set_ylabel(r"$v(t)$ [m/s]")
    ax2.set_title(error + " error between analytic and numerical solutions")

    fig.tight_layout()
    
    return None

def second_order_diff_eq_graph(
    x: ArrayLike, 
    y: ArrayLike, 
    dy: ArrayLike
) -> None:
    """
    Used to plot the solutions to a second-order differential equation.
    Plots the velocity and position.

    Parameters
    ----------
    x : array
        x values.
    y : array
        y values.
    dy : array
        First derivative values.

    Returns
    -------
    None
    """
    fig = plt.figure()
    ax = fig.add_subplot()

    ax.axhline(0, color="black")
    ax.plot(x, y, label="y", color="blue", lw=2)
    ax.plot(x, dy, label="dy/dx", color="red", lw=2)
    ax.set_xlim(x[0], x[-1])
    ax.set_xlabel(r"$x$", fontsize=20)
    ax.set_ylabel(r"$U_{\mathrm{sol}}$", fontsize=20)
    ax.set_title("Solution to second-order differential equation")
    plt.legend(loc="upper left")

    fig.tight_layout()
    
    return None

def projectile_motion_graph(
    t: ArrayLike, 
    x: ArrayLike, 
    y: ArrayLike, 
    dx: ArrayLike, 
    dy: ArrayLike
) -> None:
    """
    Used to plot different curves for projectile motion.
    First plot is y vs. x.
    Second plot is position (x and y) vs. time.
    Third plot is velocity (dx/dt and dy/dt) vs. time.

    Parameters
    ----------
    t : array
        Time values.
    x : array
        x values.
    y : array
        y values.
    dx : array
        First derivative values of x in terms of time.
    dy : array
        First derivative values of y in terms of time.

    Returns
    -------
    None
    """
    fig, ax = plt.subplots(3, figsize=(8, 8),sharex=True, sharey=False)

    ax[0].axhline(0, color="black", lw=1)
    ax[0].plot(x, y, color="green", lw=2)
    ax[0].set_xlim(0, x[-1])
    ax[0].set_ylim(0, y.max() + 0.5)
    ax[0].set_xlabel(r"$x$ [m]")
    ax[0].set_ylabel(r"$y$ [m]")
    ax[0].set_title("Projectile motion")

    ax[1].axhline(0, color="black", lw=1)
    ax[1].plot(t, x, label="x(t)", color="blue", lw=2)
    ax[1].plot(t, y, label="y(t)", color="red", lw=2)
    ax[1].set_xlim(t[0], t[-1])
    ax[1].set_xlabel(r"$t$ [s]")
    ax[1].set_ylabel(r"Position [meters]")
    ax[1].legend()

    ax[2].axhline(0, color="black", lw=1)
    ax[2].plot(t, dx, label=r"$dx/dt$", color="blue", lw=2)
    ax[2].plot(t, dy, label=r"$dy/dt$", color="red", lw=2)
    ax[2].set_xlim(t[0], t[-1])
    ax[2].set_xlabel(r"$t$ [s]")
    ax[2].set_ylabel(r"Velocity [m/s]")
    ax[2].legend()

    fig.tight_layout()
    
    return None

def free_fall_graph(
    t: ArrayLike, 
    x: ArrayLike, 
    dx: ArrayLike
) -> None:
    """
    Used to plot different curves for free-fall motion.
    First plot is position (x) vs. t.
    Second plot is velocity (dy/dt) vs. t.

    Parameters
    ----------
    t : array
        Time values.
    x : array
        x values.
    dx : array
        First derivative values of x in terms of time.

    Returns
    -------
    None
    """
    fig = plt.figure(figsize=(8, 4))

    ax1 = fig.add_subplot(1, 2, 1)
    ax1.axhline(0, color="black", lw=1)
    ax1.plot(t, x, color="blue", lw=2)
    ax1.set_xlim(t[0], t[-1])
    ax1.set_xlabel(r"$t$ [s]")
    ax1.set_ylabel(r"$x(t)$ [m]")
    ax1.set_title("Solution to Newtons equation in free-fall: \n Position")

    ax2 = fig.add_subplot(1,2,2)
    ax2.axhline(0, color="black", lw=1)
    ax2.plot(t, dx, color="red")
    ax2.set_xlim(t[0], t[-1])
    ax2.set_xlabel(r"$t$ [s]")
    ax2.set_ylabel(r"$v(t)$ [m/s]")
    ax2.set_title("Solution to Newtons equation in free-fall: \n Velocity")

    fig.tight_layout()
    
    return None


